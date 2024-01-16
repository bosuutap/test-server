from flask import Flask, request, send_file, jsonify, redirect, Response
from flask_socketio import SocketIO, send, emit, call
import time
from random import randint
from pathlib import Path

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
    def get_onliners(event):
        nonlocal sid
        sid = event
    time.sleep(5)
    if sid:
        return {"url": f"{base_url}/test/{sid}", "status":"ok"}
    else:
        return {"status": "failed"}
        

@app.route("/test/<sid>")
def handle_test(sid):
    base_url = request.url.split("/test")[0]
    result = None
    @sio.on("done")
    def get_result(data):
        nonlocal result
        result = data
    url = request.args.get("url")
    try:
        n_o = f"NO{randint(1000, 9999)}"
        sio.call("init", {"url": url, "n_o": n_o},to=sid, timeout=10)
        sio.call("done", {"n_o": n_o}, to=sid, timeout=10000)
        if not result:
            sio.call("send",{"n_o": n_o}, to=sid)
        time.sleep(2)
        image_path = Path(f"/tmp/{n_o}.png")
        image_path.write_bytes(result["result"])
        image = f"{base_url}/{n_o}.png"
        ename = result["name"]
        location = result["location"]
        org = result["org"]
        return Response(f"{image}\n{ename}\n{location}\n{org}", content_type="text/plain")
    except Exception as e:
        return str(e)
           
@app.route("/image/<image>")
def show_image(image):
    return send_file(f"/tmp/{image}", as_attachmemt=False)
        