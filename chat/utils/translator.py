from dashscope.audio.asr import (
    TranslationRecognizerCallback,
    TranscriptionResult,
    TranslationResult,
    TranslationRecognizerRealtime
)
import dashscope
from datetime import datetime

class Callback(TranslationRecognizerCallback):
    """
    语音大模型流式传输回调对象
    """
    def __init__(self, add_func):
        super().__init__()
        self.add_func = add_func

    def on_open(self) -> None:
        self.cur_id = -1
        self.time_str = ''

    def on_close(self) -> None:
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
        self.add_func(caption)

class GummyTranslator:
    """
    使用 Gummy 引擎处理英文音频流数据，并得到对应的文本对象

    初始化参数：
        add_func: 文本对象的处理回调方法
        rate: 音频采样率
        target: 翻译目标语言（zh, en, ja 等，None 表示不翻译）
    """
    def __init__(self, add_func, rate: int, target: str | None, api_key: str):
        if api_key:
            dashscope.api_key = api_key
        self.running = False
        self.translator = TranslationRecognizerRealtime(
            model = "gummy-realtime-v1",
            format = "pcm",
            sample_rate = rate,
            transcription_enabled = True,
            translation_enabled = (target is not None),
            source_language = "en",
            translation_target_languages = [target],
            callback = Callback(add_func)
        )

    def start(self):
        """启动 Gummy 引擎"""
        self.translator.start()
        self.running = True

    def send_audio_frame(self, data: bytes):
        """发送音频帧"""
        if not self.running: return
        self.translator.send_audio_frame(data)

    def stop(self):
        """停止 Gummy 引擎"""
        self.running = False
        self.translator.stop()
