from server import start_server
from chatbot import chat_bot
from utils import stdout_cmd

def main():
    audio = bytes()
    while chat_bot.status != "stop":
        while chat_bot.status == "listen":
            chunk = chat_bot.stream.read_chunk()
            if chunk == None: continue
            chat_bot.translator.send_audio_frame(chunk)
        if chat_bot.status == "answer":
            answer = chat_bot.generate_answer()
            stdout_cmd('answer', answer)
            audio = chat_bot.synthesis(answer)
        if chat_bot.status == "output":
                chat_bot.output(audio)

if __name__ == "__main__":
    start_server()
    main()
