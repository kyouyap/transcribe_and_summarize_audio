import pyaudio
import wave
import threading
import datetime
import os


class Recorder:

    def __init__(self, output_file=f"./audio/output{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.wav", channels=1, rate=16000, chunk=1024, format=pyaudio.paInt16):
        self.output_file = output_file
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.format = format

        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self._is_recording = False
        # self.wf = None

    @property
    def is_recording(self):
        return self._is_recording

    def start_recording(self):
        if self.is_recording:
            print("Already recording!")
            return

        self._is_recording = True
        self.frames = []

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        def record_loop():
            while self.is_recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

        self.thread = threading.Thread(target=record_loop)
        self.thread.start()

        print("Recording started")

    def stop_recording(self):
        if not self._is_recording:
            print("Not recording!")
            return

        self._is_recording = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped")

    def save_recording(self):
        if self._is_recording:
            print("Please stop recording before saving!")
            return
        # output_fileのディレクトリが存在しない場合は作成する
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        wf = wave.open(self.output_file, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        # self.wf = wf
        print(f"Recording saved to {self.output_file}")
