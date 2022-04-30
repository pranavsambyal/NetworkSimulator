import PhysicalLayer.devices as devices
import Utils.utils as utils

class Bridge(devices.devices):
    def __init__(self,id,address,ports=[80,8080],active=True):
        self.mac_table = {}
        self.mac_table[ports[0]] = []
        self.mac_table[ports[1]] = []
        self.ports = ports
        self.address = address
        self.id = id
        self.active = active
        self.connected_to = []
        
    def respond_arp(self,message,sender):
        ret = 0
        for i in self.connected_to:
            dev = 0
            dev = i.respond_arp(message,self)
            if dev !=0:
                ret = dev
                self.mac_table[ret.port].append(ret.address)
        return ret

    def respond_send(self,message,sender,ack_msg=False):
        if message['H2'][0] not in self.mac_table[sender.port]:
            self.mac_table[sender.port].append(message['H2'][0])
        if message['H2'][1] in self.mac_table[sender.port]:
            return 
        elif message['H2'][1] not in self.mac_table[sender.port]:
            #Send Message To Port 
            for i in self.connected_to:
                if i.port != sender.port:
                    i.respond_send(message,self,ack_msg)
        else:
            message,reciever = utils.arp_request(self,message)
            self.mac_table[reciever.port].append(message['H2'][1])
class Switch(Bridge):
    def __init__(self,id,address,ports=[80,8080,8090,8000,8070],active=True):
        self.id = id
        self.mac_table = {}
        self.address = address
        self.ports = ports
        for i in ports:
            self.mac_table[i] = []
        self.connected_to = []
        self.active = active

    def respond_send(self,message,sender,ack_msg=False):
        if message['H2'][0] not in self.mac_table[sender.port]:
            self.mac_table[sender.port].append(message['H2'][0])
        if message['H2'][1] in self.mac_table[sender.port]:
            return 
        elif message['H2'][1] not in self.mac_table[sender.port]:
            #Send Message To Port 
            forward_port = 0
            for key in self.mac_table.keys():
                if message['H2'][1] in self.mac_table[key]:
                    forward_port = key
                    break
            for i in self.connected_to:
                if i.port == forward_port:
                    i.respond_send(message,self,ack_msg)
        else:
            message,reciever = utils.arp_request(self,message)
            self.mac_table[reciever.port].append(message['H2'][1])