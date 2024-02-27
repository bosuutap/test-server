import socket
import time
import os
import json
from util import run_tcp, DataType 
from typing import List
from types import SimpleNamespace

port = os.getenv("PORT", 8080)
server = run_tcp(port)
sessions: dict = dict()

while server.running:
    conn, client = server.accept()
    bytes_data = conn.recv(10*1024*1024)
    text = bytes_data.decode('utf-8', errors="replace")
    data = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
    
    if data.type == DataType.REQ:
        sessions[data.id] = data
        server.sendto(bytes_data, data.to)
        
    elif data.type == DataType.RES:
        session = sessions.get(data.id)
        server.sendto(bytes_data, session.ip)
