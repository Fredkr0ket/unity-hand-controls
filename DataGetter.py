import socket

udpIp = "127.0.0.1"
udpPort = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((udpIp, udpPort))

while True:
    data, addr = sock.recvfrom(1024)
    print(data)