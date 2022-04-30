import random
import Utils.utils as utils
def generate_mac_address():
    """Grants A MAC Address To Each Of The Device"""
    mac = [str(random.randint(0xB,0x63)) for x in range(3)]
    return ("69:69:69:"+":".join(mac))

def generate_ip_address():
    """Grants A IP Address To Each Of The Device"""
    return ("192.168."+str(random.randint(0,255))+"."+str(random.randint(0,255)))
    
class devices:
    def __init__(self,id,address,ip,port=80,active=True):
        self.id = id
        self.address = address
        self.ip = ip
        self.port = port
        self.active = active
        self.connected_to = []
        self.arp_table = {}
    
    def make_inactive(self):
        self.active = False

    def make_active(self):
        self.active = True
    
    def respond_arp(self,message,sender):
        if message['H3'][1] == self.ip:
            print("\u001b[32m Device {} : Sent its MAC Address as its the intended destinaition  \u001b[0m".format(self.id))
            self.arp_table[message['H3'][0]] = message['H2'][0]
            return self
        else:
            print("\u001b[31m Device {} : ARP Request Rejected  as its not the intended destination\u001b[0m".format(self.id))
            return 0

    def respond_send(self,message,sender,ack_msg = False):
        if message["H2"][1] == self.address:
            print("Devive with MAC : {} Recieved Data From Source : {} ".format(message["H2"][1],message['H2'][0]))
            if not ack_msg:
                print("Sending ACK!")
                utils.send_message(self,utils.generate_ack(message),True)
        else:
            print("Device {} Dropped The Packet".format(self.id))
            
class hubs(devices):
    def __init__(self,id,port = 80,active=True):
        self.id = id
        self.active = active
        self.connected_to = []
        self.port = port

    def respond_arp(self,message,sender):
        ret=0
        for i in self.connected_to:
            dev = 0
            if i == sender:
                continue
            dev = i.respond_arp(message,self)
            if dev !=0:
                ret = dev
        return ret

    def respond_send(self,message,sender,ack_msg=False):
        for i in self.connected_to:
            if i==sender:
                continue
            i.respond_send(message,self,ack_msg)

