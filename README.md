# demo-experiment
This repository serves as a framework for running experiments on the techtile infrastructure.

To set up your own Techtile experiment, it is recommended to create your own repository by forking from this one.

Furthermore, in order to run most of the scripts, you will need to work on a the Techtile server or on your own Linux PC connected to the Techtile LAN.

## General workflow
### 1. Server setup
Your Linux workstation will henceforth be called "server". Each physical tile of the Techtile setup houses a raspberry pi. These are referred to as "clients".

Once you have created your own repository it is good to take note of the directory structure.

#### Folder description
**client:** This folder is for code that needs to run on the client. This is also a good place to store, for example, custom FPGA images for the USRP.
**data:** This folder is for raw experiment data.
**results:** This folder for processed data.
**server:** This folder is for code that runs on the server.

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
```bash
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