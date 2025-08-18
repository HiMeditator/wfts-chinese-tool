import socket
import threading
import json
from utils import stdout_cmd, stderr
from chatbot import chat_bot

def handle_client(client_socket):
    global chat_bot
    while True:
        try:
            data = client_socket.recv(8192).decode('utf-8')
            if not data:
                continue
            data = json.loads(data)

            if data['command'] == 'stop':
                if chat_bot.status == 'listen':
                    chat_bot.stop_listening()
                if chat_bot.status == 'record':
                    chat_bot.stop_recording()
                chat_bot.status = 'stop'

            elif data['command'] == 'break':
                if chat_bot.status == 'listen':
                    chat_bot.stop_listening()
                if chat_bot.status == 'record':
                    chat_bot.stop_recording()

            elif data['command'] == 'listen':
                if chat_bot.status != 'ready':
                    stderr(f'Inappropriate Status: Chatbot is not ready, current status: {chat_bot.status}.')
                    continue
                chat_bot.start_listening()
                chat_bot.status = 'listen'

            elif data['command'] == 'record':
                if chat_bot.status != 'ready':
                    stderr(f'Inappropriate Status: Chatbot is not ready, current status: {chat_bot.status}.')
                    continue
                chat_bot.start_recording()
                chat_bot.status = 'record'

            elif data['command'] == 'translate':
                options = json.loads(data['content'])
                chat_bot.translate(options['type'], options['name'], options['text'])

            elif data['command'] == 'synthesis':
                chat_bot.text = data['content']
                chat_bot.synthesis()

            elif data['command'] == 'output':
                chat_bot.output()

            else:
                stderr('Command Error: Client command not found.')

        except Exception as e:
            stderr(f'Communication error: {e}')
            chat_bot.status = 'stop'
            break

    client_socket.close()


def start_server(port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(1)
    stdout_cmd('ready')

    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.daemon = True
    client_handler.start()
