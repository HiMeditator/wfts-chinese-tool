from server import start_server
from chatbot import chat_bot
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
        
        time.sleep(0.2)

if __name__ == "__main__":
    start_server()
    main()
