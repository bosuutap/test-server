from flask import Flask, request, send_file, jsonify, redirect
from flask_socketio import SocketIO, send, emit, call
import time
from random import randint
import eventlet
eventlet.monkey_patch()

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
    base_url = request.url.replace(f"/{prefix}", "")
    sio.emit("info", prefix)
    sid = None
    @sio.on("info")
    def get_onliners(event):
        nonlocal sid
        sid = event
    time.sleep(5)
    if sid:
        return f"{base_url}/{sid}"
    else:
        return "TIMEOUT"
        

@app.route("/<sid>")
def handle_test(sid):
    base_url = request.url.replace(f"/{sid}", "")
    url = request.args.get("url")
    try:
        n_o = randint(1000, 9999)
        sio.call("init", {"url": url, "n_o": n_o},to=sid, timeout=10)
        return redirect(f"{base_url}/{sid}/{n_o}")
    except:
        return "TIMEOUT"
           
results = set()

@app.route("/<sid>/<n_o>")
def start_testing(sid, n_o):
    url = request.args.get("url")
    sio.call("done", {"n_o": n_o}, to=sid, timeout=3600)
    result = ""
    for r in results:
        if r[0] == n_o:
            result = r[1]
    return result
            
@sio.on("done")
def get_result(data):
    global results
    results.add([data["n_o"], data])
        
        