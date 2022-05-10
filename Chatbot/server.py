import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 4001  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(10240)
            print(f"{data}")
            break
            if not data:
                break
            conn.sendall(data)