from main import app, sio as socketio
import eventlet
from eventlet import wsgi
import os 

PORT = os.getenv("PORT", 8080)

if __name__ == '__main__':
    socketio.attach(app, server=wsgi_server)
    wsgi.server(eventlet.listen(('0.0.0.0', PORT)), app)