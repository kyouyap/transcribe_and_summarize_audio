import subprocess


def transcribe(model_name="base", input_file="audio.wav", output_dir="output"):
    
    command = f"./whisper.cpp/main -m whisper.cpp/models/ggml-{model_name}.bin -f {input_file} -l ja > {output_dir}"
    subprocess.run(command, shell=True)
