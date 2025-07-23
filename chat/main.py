import socket
import threading
import time
import json
from sysout import stdout, stderr

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen(1)

status = "ready"

def handle_client(client_socket):
    global status
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            data = json.loads(data)
            if data['command'] == 'stop':
                status = "stop"
            elif data['command'] == 'send':
                stdout("print", data['content'])
        except Exception as e:
            stderr(f"Communication error: {e}")
            status = "stop"
            break
    client_socket.close()

def accept_client():
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.daemon = True
    client_handler.start()


if __name__ == "__main__":
    stdout("ready")
    accept_client()
    while True:
        if status == "ready":
            pass
        else:
            break

