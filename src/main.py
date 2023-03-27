from record import *
from summary import summary
from pynput import keyboard
from transcribe import transcribe
from argparse import ArgumentParser
from wavprocessor import WavChunker
import os
import glob
from tqdm.auto import tqdm

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_file", default=None)
    parser.add_argument("-m", "--model", dest="model_name", default="base")
    parser.add_argument("-t", "--text", dest="text_file", default=None)
    args = parser.parse_args()
    model_name = args.model_name
    if args.input_file:
        input_file = args.input_file
    else:
        recorder = Recorder()

        def on_press(key):
            if key == keyboard.KeyCode.from_char('q'):
                recorder.stop_recording()
                recorder.save_recording()
                return False

        recorder.start_recording()
        print("Press 'q' to stop recording")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        input_file = recorder.output_file
    os.makedirs(input_file.replace(".wav", ""), exist_ok=True)
    if os._exists(input_file.replace(".wav", "")):
        pass
    else:
        WavChunker(input_file, input_file.replace(".wav", "/")).chunk_audio()
    if args.text_file:
        pass
    else:
        audio_files = glob.glob(input_file.replace(".wav", "") + "/*.wav")
        # 名前順にソート
        audio_files.sort()
        os.makedirs(input_file.replace(".wav", "").replace(
            "audio", "text"), exist_ok=True)
        for audio_file in tqdm(audio_files):
            transcribe(model_name, audio_file, audio_file.replace(
                "audio", "text").replace(".wav", ".txt"))
        # audio_file.replace("audio", "text").replace(".wav", ".txt")にあるテキストファイルを結合して
        # input_file.replace("audio", "text").replace(".wav", ".txt")に保存する
        text_files = glob.glob(input_file.replace(".wav", "") + "/*.txt")
        text_files.sort()
        with open(input_file.replace("audio", "text").replace(".wav", ".txt"), "w") as f:
            for text_file in text_files:
                with open(text_file, "r") as f2:
                    f.write(f2.read())

    summary(
        input_file.replace("audio", "text").replace(".wav", ".txt"),
        input_file.replace("audio", "result").replace(".wav", ".txt"))
