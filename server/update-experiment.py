import os
import sys
import yaml

# We start by setting some paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
home = os.environ["HOME"]
tile_management_base_dir = os.path.join(home, "tile-management")
tile_management_scripts_dir = os.path.join(tile_management_base_dir, "server")
tile_management_playbook_dir = os.path.join(tile_management_base_dir, "playbooks")
tile_management_inventory_dir = os.path.join(tile_management_base_dir, "inventory")
settings_path = os.path.join(project_dir, "experiment-settings.yaml")

# We look for the tile-management repo
if not os.path.isdir(tile_management_base_dir):
  print("Could not find tile-management repository at the default location (", tile_management_base_dir, ")")
  print("Did you run ./setup-server.sh with CLONE_TILE_MANAGEMENT_REPO=1 ?")
  sys.exit(-1)

# Path to the tiles inventory (inside the tile-management repo)
inventory_path = os.path.join(tile_management_inventory_dir, "hosts.yaml")

# Import code from the tile-management repo
sys.path.append(tile_management_scripts_dir)
from ansible_utils import get_target_hosts, run_playbook

# Output some general information before we start
print("Experiment project directory: ", project_dir) # should point to tile-management repo clone

# Read experiment settings
with open(settings_path, "r") as f:
    cfg = yaml.safe_load(f)

tiles = cfg.get("tiles", "")

# host list can be used to identify individual tiles from group names
# We don't need it to run ansible playbooks, but it is a first check to see if the tiles are specified correctly
host_list = get_target_hosts(inventory_path, limit=tiles, suppress_warnings=True)
print("Working on", len(host_list) ,"tile(s):", tiles)

print("Testing connectivity ... ")
playbook_path = os.path.join(tile_management_playbook_dir, "ping.yaml")

(tiles, nr_active_tiles) = run_playbook(
  project_dir,
  playbook_path,
  inventory_path,
  extra_vars=None,
  hosts=tiles,
  mute_output=True,
  suppress_warnings=True,
  cleanup=True)

if not (nr_active_tiles == len(host_list)):
  print("Unable to connect to all tiles.")
  print("Proceeding with", nr_active_tiles, "tiles(s):", tiles)