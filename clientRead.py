import socket
import pickle

ip = "127.0.0.1"  # The server's hostname or IP address
port = 12223  # The port used by the server
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as localServer:
    localServer.connect((ip, port))
    localServer.sendall(b"ping")
    data = localServer.recv(bufferSize)
    dataReceived = pickle.loads(data)
    print(dataReceived)