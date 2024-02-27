import socket
import os
from util import run_tcp, lite
from threading import Thread

port = os.getenv("PORT", 8080)
server = run_tcp(port)

def polling():
    while server.running:
        conn, client = server.accept()
        bytes_data = conn.recv(10*1024*1024)
        text = bytes_data.decode('utf-8', errors='replace')
        result = lite(text).encode('utf-8', errors='replace')
        server.send(result)
        
Thread(target=polling).start()
while True:
    pass
    