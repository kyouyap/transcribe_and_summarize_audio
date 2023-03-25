import pyaudio
import wave
import threading
from pynput import keyboard
import datetime


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
        self.recording = False

    def start_recording(self):
        if self.recording:
            print("Already recording!")
            return

        self.recording = True
        self.frames = []

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        def record_loop():
            while self.recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

        self.thread = threading.Thread(target=record_loop)
        self.thread.start()

        print("Recording started")

    def stop_recording(self):
        if not self.recording:
            print("Not recording!")
            return

        self.recording = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped")

    def save_recording(self):
        if self.recording:
            print("Please stop recording before saving!")
            return

        wf = wave.open(self.output_file, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        print(f"Recording saved to {self.output_file}")
