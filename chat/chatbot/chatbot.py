from sysaudio import AudioStream
from sysaudio import audio_output, audio_inject
from utils import GummyTranslator
from utils.sysout import stdout_obj

import dashscope
from dashscope.api_entities.dashscope_response import Message
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

class ChatBot:
    def __init__(self):
        self.status = "ready"
        self.stream = AudioStream(0)
        self.translator = GummyTranslator(
            self.add_caption,
            self.stream.RATE,
            "zh", ""
        )
        self.synthesizer = SpeechSynthesizer(
            model='cosyvoice-v2',
            voice='loongandy_v2',
            format= AudioFormat.PCM_48000HZ_MONO_16BIT
        )
        self.caption = []
        self.pointer = 0
        self.messages: list[Message] = [
            Message(role='system', content="")
        ]

    def add_system_prompt(self, prompt: str):
        """添加大模型文档的系统提示词"""
        if(self.messages[0].role == 'system'):
            self.messages[0].content = prompt

    def start_listening(self):
        """开始监听系统音频输出"""
        self.translator.start()
        self.stream.openStream()

    def add_caption(self, caption):
        """处理新识别的音频输出项"""
        if not caption['time_s']: return
        stdout_obj(caption)
        if len(self.caption) == 0:
            self.caption.append(caption)
            return
        if self.caption[-1]['time_s'] == caption['time_s']:
            self.caption.pop()
            self.caption.append(caption)
        else:
            self.caption.append(caption)

    def stop_listening(self):
        """停止监听系统音频输出"""
        self.stream.closeStream()
        self.translator.stop()

    def generate_answer(self) -> str:
        """调用 LLM 生成文本回答"""
        while self.pointer < len(self.caption):
            self.messages.append(Message(
                role='user',
                content='Stella: ' + self.caption[self.pointer]['text']
            ))
            self.pointer += 1
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=self.messages
        )
        answer: str = response.output.text # type: ignore
        self.messages.append(Message(
            role='assistant',
            content='You: ' + answer
        ))
        return answer

    def synthesis(self, text) -> bytes | None:
        """语音合成"""
        audio = self.synthesizer.call(text)
        self.status = 'synthesis'
        return audio

    def output(self, audio: bytes | None):
        """将音频数据输出到麦克风"""
        if audio:
            # audio_output(audio)
            audio_inject(audio)
        self.status = 'ready'


chat_bot = ChatBot()
