from flask import Flask, request, send_file, jsonify, redirect, Response
from flask_socketio import SocketIO, send, emit, call
import time
from random import randint
from pathlib import Path
import os
import sys

app = Flask("Transition Point")
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins='*')

@app.route("/", methods=["GET","POST"])
def post_servers():
    sio.emit("list")
    count = 0
    epoints = []
    @sio.on("list")
    def get_onliners(event):
        nonlocal count
        epoints.append(event)
        count += 1
    time.sleep(3)
    return {"count": count,"list": epoints}

@app.route("/<prefix>")
def get_sid_info(prefix):
    base_url = request.url.split("?")[0].replace(f"/{prefix}", "")
    sio.emit("info", prefix)
    sid = None
    @sio.on("info")
    def get_client_info(event):
        nonlocal sid
        if event.get("prefix") == prefix:
            sid = event.get("id")
    time.sleep(5)
    if sid:
        return {"url": f"{base_url}/test/{sid}", "status":"ok"}
    else:
        return {"status": "failed"}
        
@app.route("/test/<sid>")
def handle_test(sid):
    base_url = request.url.split("/test")[0]
    result = None
    @sio.on("test")
    def get_result(data):
        nonlocal result
        result = data
    url = request.args.get("url")
    try:
        sio.call("test", {"url": url},to=sid, timeout=3000)
        if not result:
            time.sleep(3)
        print(result)
        image = result["image"]
        name = result["name"]
        location = result["location"]
        org = result["org"]
        return {"image": image, "name": name, "location": location, "org": org}
    except Exception as e:
        return "Error:" + str(e)
        
@app.route("/reset", methods=["POST"])
def restart_server():
    os.execl(sys.executable, sys.executable, *sys.argv)
    return "Chương trình đã đóng"