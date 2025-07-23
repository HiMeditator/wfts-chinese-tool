import socket
import threading
import json
import time
from utils import stdout, stderr
from utils import global_data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen(1)

def accept_client():
    global server
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.daemon = True
    client_handler.start()

def handle_client(client_socket):
    global global_data
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                continue
            data = json.loads(data)
            if data['command'] == 'stop':
                global_data.status = "stop"
            elif data['command'] == 'send':
                stdout("print", data['content'])
            elif data['command'] == 'listen':
                global_data.startListening()
                global_data.status = "listen"
            elif data['command'] == 'convert':
                global_data.stopListening()
                stdout("print", "A Converting...")
                global_data.status = "convert"
                stdout("print", "B Converting...")
            else:
                stderr("Command not found")
        except Exception as e:
            stderr(f"Communication error: {e}")
            global_data.status = "stop"
            break
    client_socket.close()

if __name__ == "__main__":
    stdout("ready")
    accept_client()
    while global_data.status != "stop":
        while global_data.status == "listen":
            chunk = global_data.stream.read_chunk()
            if chunk == None: continue
            global_data.translator.send_audio_frame(chunk)
        if global_data.status == "convert":
            time.sleep(1)
            stdout("print", "Converting...")
