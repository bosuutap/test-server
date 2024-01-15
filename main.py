from flask import Flask, request, send_file, jsonify
from flask_socketio import SocketIO, send, emit, call
import time
from random import randint

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

@app.route("/test")
def handle_test():
    base_url = request.url.replace("/test", "")
    url = request.args.get("url")
    sid = request.args.get("id")
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
        
        