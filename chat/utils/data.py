from sysaudio.win import AudioStream
from audio2text import GummyTranslator

class GlobalData:
    def __init__(self):
        self.status = "ready"
        self.stream = AudioStream()
        self.translator = GummyTranslator(
            self.stream.RATE,
            "en", "zh", ""
        )

    def startListening(self):
        self.translator.start()
        self.stream.openStream()

    def stopListening(self):
        self.stream.stop_signal = True
        self.translator.stop()

global_data = GlobalData()
