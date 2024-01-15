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
        epoints = []
        @sio.on("online")
        def get_onliners(event):
            name = event.get("name")
            prefix = event.get("prefix")
            sid = request.sid
            epoints.append({"id":sid, "name":name, "prefix":prefix})
        start_time = time.time()
        while True:
            if time.time() - start_time == 3:
                break
        return {"count": len(epoints),"list": epoints}
    else:
        data = request.get_json()
        prefix = data.get("prefix")
        sio.emit("status", prefix)
        sid = None
        @sio.on("status")
        def if_online(ev):
            nonlocal sid
            sid = request.sid
        start_time = time.time()
        while True:
            if sid:
                break
            if time.time() - start_time == 3:
                break
        if sid:
            return base_url + str(sid)
        else:
            return "FAIL"
            
@app.route("/<sid>")
def start_testing(sid):
    url = request.args.get("url")
    result = sio.call("lite", url, to=sid)
    return jsonify(result)
            
        
        