from sysaudio import AudioStream
from sysaudio import play_both
from utils import GummyTranslator
from utils.sysout import stdout_obj, stdout_cmd

import dashscope
from dashscope.api_entities.dashscope_response import Message
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

from .llm_chat import dashscope_chat

class ChatBot:
    def __init__(self):
        self.status = "ready"
        self.stream = AudioStream(0)
        # self.stream = AudioStream(1)
        self.translator = GummyTranslator(
            stdout_obj,
            self.stream.RATE,
            "zh", ""
        )

    def start_listening(self):
        """开始监听系统音频输出"""
        self.translator.start()
        self.stream.openStream()
        # stdout(self.stream.getInfo().strip())
        stdout_cmd('status', 'listening')

    def stop_listening(self):
        """停止监听系统音频输出"""
        self.stream.closeStream()
        self.translator.stop()

    def translate(self, text: str) -> str | None:
        """翻译成英语"""
        response = dashscope.Generation.call(
            model="qwen-max",
            messages=[
                Message(
                    role="system",
                    content="将以下内容翻译成英语，不要输出任何额外的内容"
                ),
                Message(
                    role="user",
                    content=text
                )
            ]
        )
        answer: str = response.output.text # type: ignore
        stdout_cmd("translation", answer)
        self.status = "ready"


    def synthesis(self, text) -> bytes | None:
        """语音合成"""
        stdout_cmd('status', 'synthesising')
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v2',
            voice='loongandy_v2',
            format= AudioFormat.PCM_48000HZ_MONO_16BIT
        )
        audio = synthesizer.call(text)
        self.status = 'ready'
        stdout_cmd('status', self.status)
        return audio

    def output(self, audio: bytes | None):
        """将音频数据输出到麦克风"""
        stdout_cmd('status', 'outputting')
        if audio:
            play_both(audio)
        self.translator.start()
        self.status = 'ready'
        stdout_cmd('status', self.status)

chat_bot = ChatBot()
