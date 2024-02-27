import socket
import os
from util import lite
from threading import Thread

port = os.getenv("PORT", 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", port))
server.listen()
print("Server is running")

def polling():
    while server.running:
        conn, client = server.accept()
        bytes_data = conn.recv(10*1024*1024)
        text = bytes_data.decode('utf-8', errors='replace')
        result = lite(text).encode('utf-8', errors='replace')
        conn.send(result)
        
Thread(target=polling).start()
while True:
    pass
    