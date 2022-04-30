# NetworkSimulator
# [Code](/network_interface.py)
# Objective:
- Implementation of Physical layer functionalities.
  - Deliverables: The simulator is capable of:
    - Creating end devices, hubs
    - Creating connections between them to form a topology
    - Sending and receiving data
- Implementation Data Link layer functionalities.
  - Deliverables: The simulator is capable of
    - Creating layer 2 devices: bridge and switch
    - Performing address learning in case of switch
    - Implemented at least one access control protocol- Stop and Wait, Selective Repeat.
   
# Languages And Libraries
  - Language : Python 3
  - Libraries : Matplotlib, Time, Random, Networkx, Netaddr, Threading

# Documentation
All the Classes And Functions used have been written with proper documentation in the code
files. Here is the brief overview of the functionalities.
  - Class: Devices - It represents End Devices. They have various attributes like IP Address,
MAC Address, Device Id etc.
  - Class: Hubs - It represents the Hubs in the Network. It has a function to broadcast message.
  - Class : Bridges - It represents the Bridges in the Network. They have functionality to learn
MAC Address mapping to its 2 ports dynamically.
  - Class: Switch - It represents the Switches in the Network. They can map MAC Address of
devices to the multiple ports they are connected to.
  - Class: Router - It represents Router in the Network. They have various attributes like IP
Address, MAC Address, Device Id etc. They have several interface to which other devices
can be connected. They have functions to configure IP address and MAC Address to each
interface. The Routing tables can be constructed using RIP or OSPF Protocol. All of these
are based on longest subnet mask matching.
  - Class: Process - It represents all the various processes like HTTP, SSH which can be used
by the user to communicate with other hosts.
  - Function: Send Message Request/ARP Request - Each Class Has A Corresponding Method
To Respond To Request Type It Receives
  - Other Functions Used : MAC Generator, Visualize Network, Frame Message, Make
Connections etc.
# Prerequisite
- Basic knowledge of Python language and Logic of Physical and Data Link Layer.
# References
- [Course](https://piazza.com/nit_srinagar/spring2022/itt350itl355/resources)
- [Docs for plotting the topology](https://matplotlib.org/3.3.3/tutorials/index.htmlMatplotlib) 
- [Docs for IP addressing and other related functions](https://netaddr.readthedocs.io/Netaddr)
- [For information regarding how packets travel through the network](https://www.practicalnetworking.net/series/packet-traveling/packet-traveling/) 
# [Project Report](Report.pdf)
  
