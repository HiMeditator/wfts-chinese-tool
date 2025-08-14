from sysaudio import AudioStream
from sysaudio import play_both
from utils import GummyTranslator
from utils.sysout import stdout_obj, stdout_cmd
from dashscope.api_entities.dashscope_response import Message
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat


class ChatBot:
    def __init__(self):
        self.status = "ready"
        self.text = ""
        self.audio = bytes()
        self.stream0 = AudioStream(0)
        self.stream1 = AudioStream(0)
        self.translator0 = GummyTranslator(
            stdout_obj,
            self.stream0.RATE,
            "en", "zh", ""
        )
        self.translator1 = GummyTranslator(
            self.stdout_rec_obj,
            self.stream1.RATE,
            "zh", "en", ""
        )

    def start_listening(self):
        """开始监听系统音频输出"""
        self.translator0.start()
        self.stream0.openStream()
        # stdout(self.stream0.getInfo().strip())
        stdout_cmd('status', 'listening')

    def stop_listening(self):
        """停止监听系统音频输出"""
        self.stream0.closeStream()
        self.translator0.stop()
        chat_bot.status = 'ready'
        stdout_cmd('status', 'ready')

    def stdout_rec_obj(self, obj):
        """输出录音内容的对象"""
        obj['command'] = 'record'
        stdout_obj(obj)

    def start_recording(self):
        """开始监听系统音频输入"""
        self.translator1.start()
        self.stream1.openStream()
        # stdout(self.stream1.getInfo().strip())
        stdout_cmd('status', 'recording')

    def stop_recording(self):
        """停止监听系统音频输入"""
        self.stream1.closeStream()
        self.translator1.stop()
        chat_bot.status = 'ready'
        stdout_cmd('status', 'ready')

    def synthesis(self):
        """语音合成"""
        self.status = 'synthesis'
        stdout_cmd('status', 'synthesising')
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v2',
            voice='loongandy_v2',
            format= AudioFormat.PCM_48000HZ_MONO_16BIT
        )
        self.audio = synthesizer.call(self.text)
        self.status = 'ready'
        stdout_cmd('status', 'ready')

    def output(self):
        """将音频数据输出到麦克风"""
        self.status = 'output'
        stdout_cmd('status', 'outputting')
        if self.audio:
            play_both(self.audio)
        self.status = 'ready'
        stdout_cmd('status', 'ready')

chat_bot = ChatBot()
