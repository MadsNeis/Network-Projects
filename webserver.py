# Madison Neiswonger
# CS 372
# Project One : Server

import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 3490))
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

    body = b"hello"
    response = (
        "HTTP / 1.1 200 OK\r\n"
        "Content-Type: text / plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close"
        "\r\n"
    ).encode("ISO-8859-1")

    client_socket.sendall(response+body)