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


def handle_tx_start(command, args):
    print("Received tx-start command:", command, args)
    
    global got_start
    global duration
    
    got_start = True
    _, _, val_str = args[0].partition("=")
    duration = int(val_str)
    

def handle_signal(signum, frame):
    print("\nStopping client...")
    client.stop()


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

CLOCK_TIMEOUT = 1000  # 1000mS timeout for external clock locking


if __name__ == "__main__":
    client = Client(args.config_file)
    client.on("tx-start", handle_tx_start)
    client.start()
    print("Client running...")
    
    try:
        while client.running:
            if got_start:
                got_start = False
                tx(duration, tx_streamer, rate, [channel])
                client.send("tx-done")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    client.stop()
    client.join()
    print("Client terminated.")
