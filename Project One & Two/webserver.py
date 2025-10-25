# Madison Neiswonger
# CS 372
# Project Two : A Better Web Server

import socket
import os

port = int(input("Please enter port number: "))

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', port))
s.listen()

while True:
    # Call accept () to get a new connection
    client_socket, client_addr = s.accept()
    print (client_addr)

    request_data = b""
    while b'\r\n\r\n' not in request_data:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        request_data += chunk

    # Parse request header to ge file name
    header_text = request_data.decode("ISO-8859-1")
    lines = header_text.split("\r\n")
    first_line = lines[0]
    method, path, proto = first_line.split(" ", 2)

    # Strip path off for security reasons
    filename = os.path.split(path)[-1]

    # Determine type of data in file HTML or text
    name, ext = os.path.splitext(filename)
    if ext == ".html":
        content_type = "text/html; charset=ISO-8859-1"
    elif ext == ".txt":
        content_type = "text/plain; charset=ISO-8859-1"

    # Read data from the named file
    try:
        with open(filename, "rb") as fp:
            data = fp.read()

        # HTTP response packet
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        client_socket.sendall(response + data)

    except:
        body = b"404 NOT FOUND"
        response = (
            "HTTP / 1.1 404 NOT FOUND\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 13\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        client_socket.sendall(response + body)