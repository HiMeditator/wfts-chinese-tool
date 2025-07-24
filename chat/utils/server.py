import socket
import threading
import json
from chatbot import stdout, stderr
from chatbot import chat_bot

def handle_client(client_socket):
    global chat_bot
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                continue
            data = json.loads(data)
            if data['command'] == 'stop':
                chat_bot.status = "stop"
            elif data['command'] == 'prompt':
                chat_bot.add_system_prompt(data['content'])
            elif data['command'] == 'listen':
                chat_bot.start_listening()
                chat_bot.status = "listen"
            elif data['command'] == 'answer':
                chat_bot.stop_listening()
                chat_bot.status = "answer"
            else:
                stderr("Command not found")
        except Exception as e:
            stderr(f"Communication error: {e}")
            chat_bot.status = "stop"
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(1)
    stdout("ready")
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.daemon = True
    client_handler.start()
