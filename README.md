# demo-experiment
This repository serves as a framework for running experiments on the techtile infrastructure.

To set up your own Techtile experiment, it is recommended to create your own repository by forking from this one.

Furthermore, in order to run most of the scripts, you will need to work on a the Techtile server or on your own Linux PC connected to the Techtile LAN.

## General workflow
### 1. Server setup
Your Linux workstation will henceforth be called "server". Each physical tile of the Techtile setup houses a raspberry pi. These are referred to as "clients".

Once you have created your own repository it is good to take note of the directory structure.

#### Repo structure
* **client:** This folder is for code that needs to run on the client. This is also a good place to store, for example, custom FPGA images for the USRP.
* **data:** This folder is for raw experiment data.
* **results:** This folder for processed data.
* **server:** This folder is for code that runs on the server.
* **experiment-settings.yaml:** Experiment configuration file.

#### Semi-automated server setup
You can use the ```server/setup-server.sh``` script to help you setup your server so it is able to run all the necessary scripts.

```bash
cd <your-repo-folder>/server
./setup-server.sh
```

Keep in mind that the workflow for working on your experiment heavily relies on git. You can use your preferred method to commit/push your changes. However, the clients will "automatically" pull your updated repo. **This process does currently not allow to use private git repositories.**

The ```setup-server.sh``` script will create a python virtual environment and download necessary Python libraries. Once the script has been run successfully, you can activate the virtual environment:

```bash
source bin/activate
```

### 2. Client setup
Getting the clients ready to run the experiment involves several steps, which are currently handled the ```setup-clients.py``` script.

This script reads several settings from ```experiment-settings.yaml```. Make sure these are set correctly.

#### Most important settings
* ```tiles```: list of clients (or predefined groups such as "ceiling", "segmentA", etc.). This list is to be presented as a string where each name is separated by a space.
* ```extra_packages```:  list of extra packages to be installed on the client (needed to run the experiment client script).
* ```experiment_repo``` and ```organisation```: names of your GitHub repository and organisation. If you have forked your own experiment repo under "https://github.com/yourname/my-techtile-experiment", then put:
```yaml
experiment_repo: "my-techtile-experiment"
organisation: "yourname"
```

#### Script actions
The ```setup-clients.py``` script performs several actions:
* An apt update && apt upgrade to ensure all packages are up-to-date
* Installation of several extra packages. Other packages required by your client script can be specified in ```experiment-settings.yaml```, but the following packages are installed by default:
    * git
    * python3-venv
    * build-essential
    * libuhd-dev
    * python3-uhd
    * uhd-host
    * cmake
    * libboost-all-dev
* Download the repositories needed to run the experiment on the client, i.e., the [tile-management](https://github.com/techtile-by-dramco/tile-management) repo and your own experiment repo.
* Check if UHD is installed and if the UHD Python API is available. This operation will also download the necessary USRP firmware images.

Each of these steps can be run separately as well.

#### Important remark
Sometimes it is required to reboot the clients after the installation of UHD. This can be done using:
```
python reboot-clients.py
```
It is recommended to follow-up with:
```
python setup-clients.py --check-uhd-only
```

#### Usage options
```
python setup-clients.py -h
usage: setup-clients.py [-h] [--ansible-output] [--skip-apt] [--install-only] [--repos-only] [--check-uhd-only]

Setup the tiles' raspberry pi's so they can run the experiment.

This involves:
    - making sure all installed packages are up-to-date
    - installing required packages
    - pulling both the tile-management and the experiment repo
    - downloading the b210 firmware images
    - testing if the UHD python API works

options:
  -h, --help            show this help message and exit
  --ansible-output, -a  Enable ansible output
  --skip-apt, -s        Skip apt update/upgrade and apt install <extra-packages> (defined in experiment-settings.yaml)
  --install-only, -i    Run apt update/upgrade and apt install <extra-packages> (defined in experiment-settings.yaml)
  --repos-only, -r      Only pull the required repositories
  --check-uhd-only, -c  Only check if the UHD python API is available
```

### 3. Running the experiment
Running an experiment might be an iterative process.
1. Make changes to ```experiment-settings.yaml```, your client script (or both)
2. Run the experiment
3. Collect your data
4. Repeat

#### 1. Updating your experiment
If you have changed your client script's arguments, created a new client script (or renamed it), it is important to update ```experiment-settings.yaml```. For example:

```yaml
client_script_name: "my-usrp-measurement.py"
script_args:
  - "--frequency-MHz"
  - "2400"
  - "--duration-s"
  - "600"
```

Once you've made changes (step 1), it is important to push these changes to the clients. This is also a two-step process:
1. Push the modifications to your git repository using your preferred method
2. Run ```python update-experiment.py```

#### Usage options
```
python update-experiment.py -h
usage: update-experiment.py [-h] [--ansible-output]

Notify the tiles' rpi's of any updated experiment settings

This involves:
    - pulling the latest version of the experiment repo
    - installing the experiment client script

options:
  -h, --help            show this help message and exit
  --ansible-output, -a  Enable ansible output
```

#### 2. Running your experiment
Now you can start your experiment. The ```run-clients.py``` allows you to start your all your client scripts (or stop a running script).

#### Usage options
```
python run-clients.py -h
usage: run-clients.py [-h] [--ansible-output] [--start] [--stop]

Run (or halt) an experiment client script the raspberry pi's on the tiles.

options:
  -h, --help            show this help message and exit
  --ansible-output, -a  Enable ansible output
  --start               Start the script
  --stop                Stop the script
```

#### 3. Collect your data
**TODO:** No scripts for collecting your data yet.

### 4. Experiment clean-up
Once your completely finished with an experiment. It is always good to clean-up the clients so the person using them after you doesn't run into any conflicts. In order to do so, use the ```cleanup-clients.py``` script.

#### Usage options
```
python cleanup-clients.py -h
usage: cleanup-clients.py [-h] [--ansible-output]

Cleanup the home directory of the tiles' raspberry pi's.

options:
  -h, --help            show this help message and exit
  --ansible-output, -a  Enable ansible output
```




# Server–USRP Communication Standard

## General principles
- All commands are non-blocking.
- Commands are broadcast by default.
- Unicast behavior is enabled by explicitly specifying `tiles` or `hosts`.
- All time references use USRP time and assume PPS alignment.
- Commands are expected to be answered when executed via a "<command>_DONE" message, e.g., "SYNC_DONE"

---

## SYNC

Aligns all tiles to a common time reference.

```
SYNC:
  - mode: ON_NEXT_PPS | IMMEDIATE
```

Behavior:
- ON_NEXT_PPS aligns internal time at the next PPS edge.
- IMMEDIATE aligns immediately using the current PPS state (debug only).

---


## CAL


```
CAL:
  - at: <time-ms> | delay: <time-ms>
  - mode: LB
```

Behavior:

---


## PILOT

Aligns all tiles to a common time reference.

```
PILOT:
  - at: <time-ms> | delay: <time-ms>
  - tx_tiles: 
  - rx_tiles: <ALL>
  - waveform: <file name>
```

Behavior:

---

## SETUP

Loads static experiment configuration. Does not start RF activity.
```
SETUP:
  - waveform: <file_name>
  - weights: <file_name>
  - direction: tx | rx
  - tiles: ALL (default)
```

Notes:
- May be called multiple times before START.
- A new SETUP overwrites any previous setup for the addressed tiles.
- No implicit START is triggered.

---

## START

Schedules RF activity.

```
START:
  - at: <time-ms> | delay: <time-ms>
  - mode: CONTINUOUS | BURST
  - direction: tx | rx
  - duration: <time-ms>
  - tiles: ALL (default)
  - waveform: <file_name> (optional)
  - weights: <file_name> (optional)
```

Semantics:
- at is absolute USRP time.
- delay is relative to command reception time.
- CONTINUOUS runs until explicitly stopped.
- BURST stops automatically after duration.

Constraints:
- START without a prior SETUP is invalid.
- A new START replaces any pending START for the same tile and direction.

---

## STOP

Stops RF activity.
```
STOP:
  - at: <time-ms> | delay: <time-ms>
  - direction: tx | rx | both
  - tiles: ALL (default)
```
Behavior:
- Cancels running and scheduled START commands.
- both stops TX and RX simultaneously.

---

## STATUS (optional)

Queries the system state.

```
STATUS:
  - query: TIME | STATE | SETUP
  - tiles: ALL (default)
```

Returns:
- TIME returns current USRP time.
- STATE returns IDLE | ARMED | RUNNING.
- SETUP returns active waveform and weights.

---

## ABORT

Immediate safety stop.

```
ABORT:
  - tiles: ALL (default)
```

Behavior:
- Immediate RF shutdown.
- Clears all pending schedules.
- Preserves the last SETUP configuration.

---

## Typical experiment flows

Burst experiment:
```
SYNC:
  - mode: ON_NEXT_PPS

SETUP:
  - waveform: wf.iq
  - weights: bf.yml
  - direction: tx

START:
  - at: 100000
  - mode: BURST
  - direction: tx
  - duration: 1000
```

Continuous experiment:
```
SYNC:
  - mode: ON_NEXT_PPS

SETUP:
  - waveform: wf.iq
  - weights: bf.yml
  - direction: rx

START:
  - delay: 0
  - mode: CONTINUOUS
  - direction: rx

STOP:
  - delay: 5000
  - direction: rx
```
