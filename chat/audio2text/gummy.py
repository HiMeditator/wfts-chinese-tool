from dashscope.audio.asr import (
    TranslationRecognizerCallback,
    TranscriptionResult,
    TranslationResult,
    TranslationRecognizerRealtime
)
from dashscope.common.error import InvalidParameter
import dashscope
from datetime import datetime
from utils import stdout_caption, stderr

class Callback(TranslationRecognizerCallback):
    """
    语音大模型流式传输回调对象
    """
    def __init__(self):
        super().__init__()
        self.cur_id = -1
        self.time_str = ''

    def on_open(self) -> None:
        # print("on_open")
        pass

    def on_close(self) -> None:
        # print("on_close")
        pass

    def on_event(
        self,
        request_id,
        transcription_result: TranscriptionResult,
        translation_result: TranslationResult,
        usage
    ) -> None:
        caption = {}
        if transcription_result is not None:
            caption['index'] = transcription_result.sentence_id
            caption['text'] = transcription_result.text
            if caption['index'] != self.cur_id:
                self.cur_id = caption['index']
                cur_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                caption['time_s'] = cur_time
                self.time_str = cur_time
            else:
                caption['time_s'] = self.time_str
            caption['time_t'] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            caption['translation'] = ""

        if translation_result is not None:
            lang = translation_result.get_language_list()[0]
            caption['translation'] = translation_result.get_translation(lang).text

        caption['command'] = "caption"
        stdout_caption(caption)

class GummyTranslator:
    """
    使用 Gummy 引擎处理音频数据，并在标准输出中输出与 Auto Caption 软件可读取的 JSON 字符串数据

    初始化参数：
        rate: 音频采样率
        source: 源语言代码字符串（zh, en, ja 等）
        target: 目标语言代码字符串（zh, en, ja 等，None 表示不翻译）
    """
    def __init__(self, rate, source, target, api_key):
        if api_key:
            dashscope.api_key = api_key
        self.running = False
        self.translator = TranslationRecognizerRealtime(
            model = "gummy-realtime-v1",
            format = "pcm",
            sample_rate = rate,
            transcription_enabled = True,
            translation_enabled = (target is not None),
            source_language = source,
            translation_target_languages = [target],
            callback = Callback()
        )

    def start(self):
        """启动 Gummy 引擎"""
        self.translator.start()
        self.running = True

    def send_audio_frame(self, data):
        """发送音频帧"""
        if not self.running: return
        try:
            self.translator.send_audio_frame(data)
        except InvalidParameter:
            stderr("Gummy: Invalid parameter")

    def stop(self):
        """停止 Gummy 引擎"""
        self.running = False
        self.translator.stop()
