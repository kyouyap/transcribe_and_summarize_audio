from record import *
from summary import summary
from pynput import keyboard
from transcribe import transcribe
from argparse import ArgumentParser


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

    if args.text_file:
        pass
    else:
        transcribe(model_name, input_file, input_file.replace(
            "audio", "text").replace(".wav", ".txt"))

    summary(
        input_file.replace("audio", "text").replace(".wav", ".txt"),
        input_file.replace("audio", "result").replace(".wav", ".txt"))
