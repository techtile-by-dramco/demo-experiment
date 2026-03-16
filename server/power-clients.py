import os
import sys
import yaml
import argparse
import config

def get_poe_info(inventory, host):
    hosts = inventory["all"]["hosts"]
    midspans = inventory["all"]["vars"]["midspans"]

    if host not in hosts:
        raise ValueError(f"Host {host} not found")

    host_data = hosts[host]

    poe_port = host_data.get("poe-port")
    midspan = host_data.get("midspan")

    if not midspan:
        return None

    midspan_ip = midspans[midspan]["ip"]

    return poe_port, midspan_ip


parser = argparse.ArgumentParser(
    description="Control power of the tiles. CAREFUL! This will power up/down everything on the tile(s)."
)

parser.add_argument(
    "--power-up", "-u",
    action="store_true",
    help="Power-up a tile."
)

parser.add_argument(
    "--power-down", "-d",
    action="store_true",
    help="Power-down a tile."
)

args = parser.parse_args()

# We start by setting some paths
settings_path = os.path.join(config.PROJECT_DIR, "experiment-settings.yaml")

# Check if the tile-management repo is in the default location (no use in continuing if it's not)
if not config.check_tile_management_repo():
    sys.exit(config.ERRORS["REPO_ERROR"])

# Import code from the tile-management repo
sys.path.append(config.UTILS_DIR)
from ansible_utils import get_target_hosts
from midspan_utils import midspan_support_class

# Output some general information before we start
print("Experiment project directory: ", config.PROJECT_DIR) # should point to tile-management repo clone

# Read experiment settings
with open(settings_path, "r") as f:
    experiment_settings = yaml.safe_load(f)

tiles = experiment_settings.get("tiles", "")
if len(tiles) == 0:
    print("The experiment doesn't target any tiles.")
    sys.exit(config.ERRORS["NO_TILES_ERROR"])
test_connectivity = experiment_settings.get("test_connectivity", True)
halt_on_connectivity_failure = experiment_settings.get("halt_on_connectivity_failure", True)

# host list can be used to identify individual tiles from group names
# We don't need it to run ansible playbooks, but it is a first check to see if the tiles are specified correctly
host_list = get_target_hosts(config.INVENTORY_PATH, limit=tiles, suppress_warnings=True)
print("Working on", len(host_list) ,"tile(s):", tiles)

with open(config.INVENTORY_PATH)as f:
    inventory = yaml.safe_load(f)

snmp_user = os.getenv("SNMP_USER")
snmp_password = os.getenv("SNMP_PASSWORD")

if snmp_user is None:
    raise RuntimeError("SNMP_USER environment variable is not set")
if snmp_password is None:
    raise RuntimeError("SNMP_PASSWORD environment variable is not set")

midspan = midspan_support_class(snmp_user, snmp_password)

for host in host_list:
    (poe_port, midspan_ip) = get_poe_info(inventory, host)
    print("midspan ip:", midspan_ip)
    print("poe port:", poe_port)
    
    print("port status:", midspan.getPortStatusOld(midspan_ip, poe_port))
          