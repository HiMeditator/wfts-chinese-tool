import pyaudiowpatch as pyaudio
import numpy as np
from utils import stdout

def audio_output(audio: bytes) -> None:
    """向输出设备播放音频"""
    stdout("Audio playing...")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        output=True
    )
    stream.write(audio)
    stream.close()
    p.terminate()
    stdout("Audio played.")

def mic_inject(audio: bytes) -> None:
    """将音频数据注入到麦克风输入流中"""
    pass

