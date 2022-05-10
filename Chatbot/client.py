import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 4001  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    #data = s.recv(10240)

#print(f"Received {data!r}")