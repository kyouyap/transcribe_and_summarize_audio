import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

class WavProcessor:
    def __init__(self, input_file, output_file, silence_threshold=-50, min_silence_length=500, audio_file_type="wav"):
        self.input_file = input_file
        self.output_file = output_file
        self.silence_threshold = silence_threshold
        self.min_silence_length = min_silence_length
        self.audio_file_type = audio_file_type

    def remove_silence(self):
        audio = AudioSegment.from_file(self.input_file, format=self.audio_file_type)
        non_silent_slices = split_on_silence(audio, min_silence_len=self.min_silence_length, silence_thresh=self.silence_threshold, keep_silence=0)

        processed_audio = AudioSegment.empty()
        for non_silent_slice in non_silent_slices:
            processed_audio += non_silent_slice
        
        # サンプリングレートを 16 kHz に変更
        processed_audio = processed_audio.set_frame_rate(16000)

        processed_audio.export(self.output_file, format="wav")
