# import sockets module
import socket

# function to get the local ip address
def get_local_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return_var = s.getsockname()[0]
    s.close()
    return return_var

# initialize udp socket object and bind the socket to the localhost at port 49276
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 49276)
udp_socket.bind(server_address)
print('Connect any clients to ' + str(get_local_address()))

# list of client addresses
clients = []

# function to find an element in a given list
def find(list, element):
    for i in range(len(list)):
        if list[i] == element:
            return i

# host games until the user declines to play another
# while input('Would you like to host another game? ').upper() == 'YES':
while True:
    print('Waiting for client connections...')
    # gamestate variable string
    gamestate = 'PENDING'
    # pass packets back and forth until the GAME_EXIT signal arrives from the master client
    while gamestate != 'FINISHED':
        # receive incoming packages
        data, address = udp_socket.recvfrom(4096)
        # if data was received, check if the address should be added to clients list
        # if the game is in progress, send packages between clients to facilitate gameplay
        # if the GAME_EXIT signal is received, pass it to all clients then exit game
        if data:
            if gamestate == 'PENDING':
                if address not in clients and len(clients) < 2:
                    print('New connection from ' + address[0] + ' on port', address[1])
                    clients.append(address)
                    if len(clients) == 1:
                        print('Primary client connected. Waiting for secondary connection.')
                        udp_socket.sendto('PRIMARY'.encode('utf-8'), address)
                    else:
                        print('Secondary client connected. Starting Game!')
                        udp_socket.sendto('SECONDARY'.encode('utf-8'), address)
                        for client in clients:
                            print('Sending GAME_BEGIN message to ' + client[0] + ' on port', client[1])
                            message = 'GAME_BEGIN'
                            udp_socket.sendto(message.encode('utf-8'), client)
                        gamestate = 'PLAYING'
            elif address[0] == clients[0][0] and data.decode('utf-8') == 'GAME_EXIT':
                print('Received exit signal from primary client. Exiting game!')
                for client in clients:
                    udp_socket.sendto(data, address)
                gamestate = 'FINISHED'
            elif gamestate == 'PLAYING':
                destination_address = clients[find(clients, address)-1]
                print('Sending data from ' + address[0] + ':' + str(address[1]) + ' to ' + destination_address[0] + ':' + str(destination_address[1]))
                udp_socket.sendto(data, destination_address)
