from netaddr import IPNetwork

def make_packets(sender_device,receiver_device,message):
    message = {'Data':message,'H3':[sender_device.ip,receiver_device.ip],'H2':[sender_device.address]}
    return message
def make_frames(receiver_device_mac,message):
    message['H2'].append(receiver_device_mac.address)
    return message

def arp_request(device,message):
    ret = 0
    for i in device.connected_to:
        ret = i.respond_arp(message,device)
        if ret != 0:
            message['H2'].append(ret.address)
    print("\n")
    return message

def send_message(d1,message,ack_msg=False):
    print("\u001b[34m")
    print(message)
    print("\u001b[30m")
    for i in d1.connected_to:
        i.respond_send(message,d1,ack_msg)

def swap_address(array):
    temp = array[0]
    array[0] = array[1]
    array[1] = temp
    return array

def generate_ack(message):
    message['Data'] = 'ACK'
    message['H3'] = swap_address(message['H3'])
    message['H2'] = swap_address(message['H2'])
    return message

def check_subnet(ip1,ip2):
    # 225 = Broadcast Address, 0 = Network Address
    subnet = "255.255.0.0"
    if IPNetwork("{}/{}".format(ip1,subnet)) == IPNetwork("{}/{}".format(ip2,subnet)):
        return True
    return False
