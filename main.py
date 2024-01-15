from flask import Flask, request, send_file
from flask_socketio import SocketIO, send, emit, call
import time

app = Flask("Transition Point")
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins='*')

@app.route("/", methods=["GET","POST"])
def post_servers():
    if request.method == "GET":
        sio.emit("list")
        epoints = []
        @sio.on("online")
        def get_onliners(event):
            name = event.get("name")
            key = event.get("key")
            sid = request.sid
            epoints.append({"id":sid, "name":name, "key":key})
        start_time = time.time()
        while True:
            if time.time() - start_time == 3:
                break
        return {"count": len(epoints),"list": epoints}
        
        