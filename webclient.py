# Madison Neiswonger
# CS 372
# Project One : Web Client

import socket

host = "127.0.0.1"
port_input = input("What port? : ")
port = int(port_input)

s = socket.socket()
s.connect((host, port))

request = "GET / HTTP/1.0\r\nhost: " + host + "\r\nConnection: close\r\n\r\n"
s.sendall(request.encode("ISO-8859-1"))

response = b""

while True:
    data = s.recv(4096)
    if len(data) == 0:
        break
    response += data
s.close()


print(response.decode("ISO-8859-1"))