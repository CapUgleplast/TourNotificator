import socket

HOST = '0.0.0.0'   # Listen on all network interfaces
PORT = 8080 # Port number to listen on

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to a specific network interface and port number
    s.bind((HOST, PORT))
    print(f"Listening on port {PORT}...")
    # Listen for incoming connections
    s.listen()
    # Accept incoming connections
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    # Receive data from the client
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data: {data.decode('utf-8').strip()}")