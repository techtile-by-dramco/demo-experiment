import os
import sys
import yaml
import config

# We start by setting some paths
settings_path = os.path.join(config.PROJECT_DIR, "experiment-settings.yaml")

# Check if the tile-management repo is in the default location (no use in continuing if it's not)
if not config.check_tile_management_repo():
    sys.exit(-1)

# Import code from the tile-management repo
sys.path.append(config.UTILS_DIR)
from ansible_utils import get_target_hosts, run_playbook

# Output some general information before we start
print("Experiment project directory: ", config.PROJECT_DIR) # should point to tile-management repo clone

# Read experiment settings
with open(settings_path, "r") as f:
    experiment_settings = yaml.safe_load(f)

tiles = experiment_settings.get("tiles", "")
if len(tiles) == 0:
    print("The experiment doesn't target any tiles.")
    sys.exit(-2)
test_connectivity = experiment_settings.get("test-connectivity", True)
halt_on_connectivity_failure = experiment_settings.get("halt-on-connectivity-failure", True)

# host list can be used to identify individual tiles from group names
# We don't need it to run ansible playbooks, but it is a first check to see if the tiles are specified correctly
host_list = get_target_hosts(config.INVENTORY_PATH, limit=tiles, suppress_warnings=True)
print("Working on", len(host_list) ,"tile(s):", tiles)

# First we test connectivity
nr_active_tiles = 0
if test_connectivity:
    print("Testing connectivity ... ")
    playbook_path = os.path.join(config.PLAYBOOK_DIR, "ping.yaml")

    (tiles, nr_active_tiles) = run_playbook(
        config.PROJECT_DIR,
        playbook_path,
        config.INVENTORY_PATH,
        extra_vars=None,
        hosts=tiles,
        mute_output=True,
        suppress_warnings=True,
        cleanup=True
    )

    if not (nr_active_tiles == len(host_list)):
        print("Unable to connect to all tiles.")
        if halt_on_connectivity_failure:
            print("Aborting (halt-on-connectivity-failure = True)")
            # Print active tiles
            active_list = tiles.split(' ')
            print("Active tiles:", tiles)
            # Print inactive tiles
            inactive_list = ""
            for t in host_list:
                if str(t) not in active_list:
                    if len(inactive_list) > 0:
                        inactive_list += " "
                    inactive_list += str(t)
            print("Inactive tiles:", inactive_list)
            sys.exit(-3)
        else:
            print("Proceeding with", nr_active_tiles, "tiles(s):", tiles)
            
prev_nr_active_tiles = nr_active_tiles

print("Cleaning tile home-directory ... ")
print("TODO: handle experiment-service. -  For now, we don't clean tile-management.")
playbook_path = os.path.join(config.PLAYBOOK_DIR, "clean-home.yaml")

(tiles, nr_active_tiles) = run_playbook(
  config.PROJECT_DIR,
  playbook_path,
  config.INVENTORY_PATH,
  extra_vars=None,
  hosts=tiles,
  mute_output=True,
  suppress_warnings=True,
  cleanup=True)

if not (nr_active_tiles == prev_nr_active_tiles):
  print("Unable to connect to all tiles.")

print("Cleaned the home directory of tiles(s):", tiles)