from server import start_server
from chatbot import chat_bot
from utils import stdout

def main():
    audio = bytes()
    while chat_bot.status != "stop":
        while chat_bot.status == "listen":
            chunk = chat_bot.stream.read_chunk()
            if chunk == None: continue
            chat_bot.translator.send_audio_frame(chunk)
        if chat_bot.status == "answer":
            stdout('Answering...')
            answer = chat_bot.generate_answer()
            stdout(answer)
            stdout('Synthesizing...')
            audio = chat_bot.synthesis(answer)
            stdout('Sythesized')
        if chat_bot.status == "output":
                chat_bot.output(audio)

if __name__ == "__main__":
    start_server()
    main()
