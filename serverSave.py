import socket

ip = "127.0.0.1"
port = 12222
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as localServer:
    localServer.bind((ip, port))
    localServer.listen()
    clientConnection, clientAddress = localServer.accept()
    with clientConnection:
        #print(f"Connected by {clientAddress}")
        f = open("weekly.txt", "wb")
        while True:
            data = clientConnection.recv(bufferSize)
            if not data:
                break
            f.write(data)
        f.close()
        #clientConnection.close()