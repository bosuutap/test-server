from main import app, sio as socketio
import os 

PORT = os.getenv("PORT", 8080)

if __name__ == '__main__':
    # Use eventlet as the worker for Waitress to support WebSockets
    import eventlet
    from eventlet import wsgi
    # Create a WSGI server instance
    wsgi_server = eventlet.listen(('0.0.0.0', PORT))
    # Wrap the Flask app with Socket.IO
    socketio.attach(app, server=wsgi_server)
    # Run the eventlet WSGI server
    eventlet.wsgi.server(wsgi_server, app)