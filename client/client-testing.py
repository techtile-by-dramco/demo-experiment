from utils.client_com import Client
import signal
import time
import sys
import argparse, shlex
from datetime import datetime, timezone, timedelta
import uhd
import numpy as np
import yaml

"""Parse the command line arguments"""
parser = argparse.ArgumentParser()
parser.add_argument("--config-file", type=str)

args = parser.parse_args()

client = None 
got_start = False


def handle_usrp_sync(command, args):
    print("Received usrp_sync command:", command, args)
    
    client.send("usrp_ack")
    global got_start
    
    got_start = True


def handle_signal(signum, frame):
    print("\nStopping client...")
    client.stop()


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

CLOCK_TIMEOUT = 1000  # 1000mS timeout for external clock locking


if __name__ == "__main__":
    client = Client(args.config_file)
    client.on("usrp_sync", handle_usrp_sync)
    client.start()
    print("Client running...")
    
    try:
        while client.running:
            if got_start:
                got_start = False
                time.sleep(5)
                client.send("usrp_done")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    client.stop()
    client.join()
    print("Client terminated.")
