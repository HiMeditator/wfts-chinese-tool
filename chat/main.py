from utils import start_server
from chatbot import chat_bot


if __name__ == "__main__":
    start_server()
    while chat_bot.status != "stop":
        while chat_bot.status == "listen":
            chunk = chat_bot.stream.read_chunk()
            if chunk == None: continue
            chat_bot.translator.send_audio_frame(chunk)
        if chat_bot.status == "answer":
            chat_bot.answer()

