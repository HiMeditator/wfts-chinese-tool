from sysaudio.win import AudioStream
from audio2text import GummyTranslator
import dashscope
from dashscope.api_entities.dashscope_response import Message
from chatbot.sysout import stdout_caption, stdout

class ChatBot:
    def __init__(self):
        self.status = "ready"
        self.stream = AudioStream(1)
        self.translator = GummyTranslator(
            self.add_caption,
            self.stream.RATE,
            "zh", ""
        )
        self.system_prompt = ""
        self.caption = []
        self.pointer = 0
        self.messages: list[Message] = [
            Message(role='system', content=self.system_prompt)
        ]

    def start_listening(self):
        """开始监听系统音频输出"""
        self.translator.start()
        self.stream.openStream()

    def add_caption(self, caption):
        """将系统音频输出识别出的字幕添加到列表中"""
        if not caption['time_s']: return
        stdout_caption(caption)
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

    def add_system_prompt(self, prompt):
        """添加大模型文档的系统提示词"""
        self.system_prompt = prompt
        if(self.messages[0].role == 'system'):
            self.messages[0].content = prompt

    def answer(self):
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
        self.messages.append(Message(
            role='assistant',
            content='You: ' + response.output.text # type: ignore
        ))
        stdout('print', response.output.text) # type: ignore
        self.status = 'convert'

    def convert(self):
        pass

chat_bot = ChatBot()
