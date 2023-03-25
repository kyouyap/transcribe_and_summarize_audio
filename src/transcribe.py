import subprocess


def transcribe(model_name="base", input_file="audio.wav", output_file="output.txt"):
    #  ./whisper.cpp/main -m whisper.cpp/models/ggml-medium.bin -f audio/output2.wav -l auto > text/output2.txt
    command = f"./whisper.cpp/main -m whisper.cpp/models/ggml-{model_name}.bin -f {input_file} -l auto > {output_file}"
    subprocess.run(command, shell=True)
