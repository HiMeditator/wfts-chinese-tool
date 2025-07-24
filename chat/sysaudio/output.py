import pyaudiowpatch as pyaudio
from utils import stdout, stderr
import json

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

def audio_inject(audio: bytes) -> None:
    """将音频数据注入到麦克风输入流中"""
    stdout("Audio injecting...")
    p = pyaudio.PyAudio()
    num = p.get_device_count()
    index = -1
    for i in range(num):
        dev_info = p.get_device_info_by_index(i)
        dev_name = dev_info['name'].lower()
        if ('cable' in dev_name) and ('input' in dev_name):
            stdout(dev_name)
            index = i
            break
    if index == -1:
        stderr("CABLE Input (VB-Audio Virtual Cable) not found")
        return
    stdout(json.dumps(p.get_device_info_by_index(index)))
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        output=True,
        output_device_index=index
    )
    stream.write(audio)
    stdout("Audio injected.")

