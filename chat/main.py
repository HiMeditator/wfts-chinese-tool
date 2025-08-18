from server import start_server
from chatbot import chat_bot
from utils import stdout
import argparse
import time

def main():
    while chat_bot.status != "stop":
        while chat_bot.status == "listen":
            chunk = chat_bot.stream0.read_chunk()
            if chunk == None: continue
            chat_bot.translator0.send_audio_frame(chunk)
        
        while chat_bot.status == "record":
            chunk = chat_bot.stream1.read_chunk()
            if chunk == None: continue
            chat_bot.translator1.send_audio_frame(chunk)
        
        while chat_bot.status == "synthesis":
            chat_bot.synthesis()

        while chat_bot.status == "output":
            chat_bot.output()

        time.sleep(0.2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert system audio stream to text')
    parser.add_argument('-p', '--port', default=8080, help='The port to run the server on')
    args = parser.parse_args()
    stdout(f"Socket Port: {args.port}")
    start_server(int(args.port))
    main()
