import socket
import pickle
import json

ip = "127.0.0.1"
port = 12223
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as localServer:
    localServer.bind((ip, port))
    localServer.listen()
    clientConnection, clientAddress = localServer.accept()
    with clientConnection:
        #print(f"Connected by {clientAddress}")
        f = open("weekly.txt", "rb")
        while True:
            data = clientConnection.recv(bufferSize)
            if not data:
                break
            # read binary date
            buffer = pickle.load(f)
            # read json
            #buffer = json.load(f)
            bufferAcross = pickle.dumps(buffer)
            clientConnection.sendall(bufferAcross)
        f.close()

