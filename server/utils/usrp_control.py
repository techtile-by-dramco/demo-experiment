from utils.server_com import ServerSideCom
from enum import Enum
import json

class USRP_Control:
    class Commands(Enum):
        SYNC = "usrp_sync"
        CAL = "usrp_cal"
        PILOT = "usrp_pilot"
        UNDEFINED = ""
        
    class Responses(Enum):
        ACK = "usrp_ack"
        DONE = "usrp_done"

    class ReturnCodes(Enum):
        OK = 1
        UNKNOWN_ERROR = 255
    
    def __init__(self, server_side_com=None, silent=True):
        if not server_side_com:
            raise ValueError(f"{__class__}: server_side_com not specified")
        
        self.server = server_side_com
        self.server.on(self.Responses.ACK, self._handle_ack)
        self.server.on(self.Responses.DONE, self._handle_done)
        self.required_hosts = []
        
    def start(self):
        if not self.server.running:
            print("starting server com")
            self.server.start()
    
    def set_required_hosts(self, host_list = []):
        self.required_hosts = host_list
    
    def send_command(self, command: Commands = Commands.UNDEFINED, **args):
        tiles = None
        if args:
            try:
                hosts = args.get("tiles", None)
            except ValueError as e:
                hosts = None
        
        connected_hosts = self.server.get_connected()
        
        print(connected_hosts)
        print(self.required_hosts)
        
        if tiles:
            for tile in tiles:
                print("server send to", tile)
            #self.server.send("")
            print(json.dumps(args))
        else:
            #self.server.broadcast("")
            print("server broadcast")
        
    def _handle_ack(self):
        print("ack handled")
        
    def _handle_done(self):
        print("done handled")