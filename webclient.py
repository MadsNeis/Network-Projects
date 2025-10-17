# Madison Neiswonger
# CS 372
# Project Two : A Better Web Server

import socket

host = "localhost"
port_input = input("What port? : ")
port = int(port_input)

s = socket.socket()
s.connect((host, port))

request = "GET /file2.html HTTP/1.0\r\nhost: " + host + "\r\nConnection: close\r\n\r\n"
s.sendall(request.encode("ISO-8859-1"))

response = b""

while True:
    data = s.recv(4096)
    if len(data) == 0:
        break
    response += data
s.close()


print(response.decode("ISO-8859-1"))