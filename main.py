from flask import Flask, request, send_file, jsonify
from flask_socketio import SocketIO, send, emit, call
import time

app = Flask("Transition Point")
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins='*')

@app.route("/", methods=["GET","POST"])
def post_servers():
    base_url = request.url.split("://")[1].split("/")[0]
    if request.method == "GET":
        sio.emit("list")
        count = 0
        epoints = []
        @sio.on("online")
        def get_onliners(event):
            nonlocal count
            epoints.append(event)
            count += 1
        time.sleep(3)
        return {"count": count,"list": epoints}
    else:
        data = request.get_json()
        prefix = data.get("prefix")
        sio.emit("status", prefix)
        sid = None
        @sio.on("status")
        def if_online(ev):
            nonlocal sid
            sid = request.sid
        before = time.time()
        while time.time() - before > 3 or sid:
            break
        if sid:
            return base_url + str(sid)
        else:
            return "TIMEOUT"
            
@app.route("/<sid>")
def start_testing(sid):
    url = request.args.get("url")
    sio.emit("lite", {"data": url}, to=sid)
    result = None
    @sio.on("lite")
    def get_result(data):
        nonlocal result
        if request.sid == sid:
            result = data
    start = time.time()
    while not result or time.time() - start < 3600:
        continue
    return jsonify(result)
            
        
        