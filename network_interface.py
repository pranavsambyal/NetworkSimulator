import PhysicalLayer.devices as devices
import networkx as nx
import matplotlib.pyplot as plt
import DataLinkLayer.layer2_devices as layer2_devices
import Utils.utils as utils

class Network:
    def __init__(self):
        self.num_devices = 0
        self.num_hubs = 0
        self.num_bridges = 0
        self.num_switches = 0
        self.__devices = []
        self.total_devices = 0
        self.connections = []

    def add_device(self,device):
        self.num_devices += 1
        self.__devices.append(device)
        self.total_devices += 1
        self.connections.append([])

    def add_hub(self,hub):
        self.num_hubs += 1
        self.__devices.append(hub)
        self.total_devices += 1
        self.connections.append([])

    def add_bridge(self,bridge):
        self.num_bridges += 1 
        self.__devices.append(bridge)
        self.total_devices += 1
        self.connections.append([])

    def add_switch(self,swtich):
        self.num_switches += 1
        self.__devices.append(swtich)
        self.total_devices += 1
        self.connections.append([])

    def check_valid_device(self,d1,d2):
        if d1 >= self.total_devices or d2 >= self.total_devices:
            raise Exception("Device Dosent Exist! Please Enter Valid Device Numbers.")

    def check_device_status(self,d1,d2):
        if not ((self.__devices[d1].active) and (self.__devices[d2].active)):
            raise Exception("Device Not Active. Please Check Device Status")

    def check_connection(self,d1,d2):
        #Check if it is possible to send message via any connection.
        for i in self.connections[d1]:
            if type(i) == devices.hubs:
                i.broadcast(d1,d2)
                break
        if self.__devices[d2] in self.connections[d1]:
            return
        else:
            raise Exception("No Connection Between Two Devices!")

    def make_connection(self,d1,d2):
        try:
            self.check_valid_device(d1,d2)
            self.connections[d1].append(self.__devices[d2])
            self.__devices[d1].connected_to.append(self.__devices[d2])
            self.connections[d2].append(self.__devices[d1])
            self.__devices[d2].connected_to.append(self.__devices[d1])
        except Exception as e:
            print("Invalid Input! Please Check And Enter Again!")
            print(e)

    def send_msg(self,sender_device,receiver_device,message):
        message = utils.make_packets(self.__devices[sender_device],self.__devices[receiver_device],message)
        # # check whether the device is in same network or not:  TODO: SUBNET FOR ROUTERS!
        if self.__devices[receiver_device].ip in self.__devices[sender_device].arp_table.keys():
            print("\u001b[33m Not need to send ARP request as the table is already populated \u001b[30m")
            message['H2'].append(self.__devices[sender_device].arp_table[self.__devices[receiver_device].ip])
        else:
            message = utils.arp_request(self.__devices[sender_device],message)
            self.__devices[sender_device].arp_table[self.__devices[receiver_device].ip] = self.__devices[receiver_device].address
        try:
            if len(message['H2']) == 1:
                raise Exception("NO Connection Exists!")
            self.check_valid_device(sender_device,receiver_device)
            self.check_device_status(sender_device,receiver_device)
            utils.send_message(self.__devices[sender_device],message)
        except Exception as e:
            print(e)


#Driver Code Example
def main():
    Star = Network()
    Star.add_device(devices.devices(Star.total_devices,devices.generate_mac_address(),'10.0.0.1',8080))
    Star.add_device(devices.devices(Star.total_devices,devices.generate_mac_address(),'10.0.0.2',8080))
    Star.add_device(devices.devices(Star.total_devices,devices.generate_mac_address(),'10.0.0.3',8080))
    Star.add_device(devices.devices(Star.total_devices,devices.generate_mac_address(),'10.1.0.1'))
    Star.add_device(devices.devices(Star.total_devices,devices.generate_mac_address(),'10.2.0.1'))
    Star.add_hub(devices.hubs(Star.total_devices,8080))
    Star.add_hub(devices.hubs(Star.total_devices,80))
    Star.add_bridge(layer2_devices.Bridge(Star.total_devices,devices.generate_mac_address()))
    Star.add_switch(layer2_devices.Switch(Star.total_devices,devices.generate_mac_address()))
    Star.make_connection(5,7)
    Star.make_connection(6,7)
    Star.make_connection(0,5)
    Star.make_connection(1,5)
    Star.make_connection(2,5)
    Star.make_connection(3,6)
    Star.make_connection(4,6)
    print("----Trying to send 1st message----\n\n")
    Star.send_msg(1,2,"Pranav")
    print("\n\n----Trying to send 2nd message----\n\n")
    Star.send_msg(1,3,"Daman")
    print("\n\n----Trying to send 3rd message----\n\n")
    Star.send_msg(1,3,"Daman")


if __name__=="__main__":
    main()