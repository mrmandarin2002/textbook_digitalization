# import neccessary functions and classes
from datetime import datetime
import socket

# import database interaction functions
from interactions import *

# function to get the current time
def get_time():
    return str(datetime.now()).split()[1].split(".")[0]+" "

# function to get the local ip address
def get_local_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return_var = s.getsockname()[0]
    s.close()
    return return_var

# initialize udp socket object and bind the socket to the localhost at port 7356
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 7356)
udp_socket.bind(server_address)
print(get_time()+"Server socket initialized")
print(get_time()+"Connect all clients to " + str(get_local_address()))

# list of client addresses
clients = []

# main server loop
print(get_time()+"Starting main server loop...")
while True:
    # receive incoming packages
    data, address = udp_socket.recvfrom(4096)
    # process any received data
    if data:
        print(get_time()+"Received data from: "+address[0]+":"+str(address[1]))
        # if the address of the received data does not exist in clients, add it before continuing
        if address not in clients:
            clients.append(address)
        # process the command request
        decoded_data = data.decode("utf-8")
        udp_socket.sendto(interact[decoded_data.split(";")[0]](decoded_data.split(";")[1].split("|")).encode("utf-8"), address)
