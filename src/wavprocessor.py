from pydub import AudioSegment
from pydub.silence import split_on_silence


class WavChunker:
    def __init__(self, input_file, output_folder, silence_threshold=-50, min_silence_length=500):
        self.input_file = input_file
        self.output_folder = output_folder
        self.silence_threshold = silence_threshold
        self.min_silence_length = min_silence_length

    def _split_audio(self, audio):
        return split_on_silence(audio,
                                min_silence_len=self.min_silence_length,
                                silence_thresh=self.silence_threshold)

    def chunk_audio(self):
        audio = AudioSegment.from_wav(self.input_file)
        chunks = self._split_audio(audio)

        for i, chunk in enumerate(chunks):
            # 名前はchunk001.wavのようにする
            chunk.export(
                f"{self.output_folder}/chunk{i:03d}.wav", format="wav")
