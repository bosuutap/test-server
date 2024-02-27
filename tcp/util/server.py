import socket
import threading

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True

        while self.running:
            client_socket, client_address = self.server_socket.accept()
            # Xử lý kết nối từ client

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

def run_tcp(port):
    server = TCPServer('0.0.0.0', port)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    return server