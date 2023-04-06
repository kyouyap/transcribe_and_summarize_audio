import openai
import os
import subprocess
import pandas as pd
import re
import csv


def parse_transcription_csv(text: str) -> str:
    pattern = re.compile(
        r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})]  (.*)')

    transcription = ""
    
    for row in text.splitlines():
        line = ''.join(row)
        match = pattern.match(line)
        if match:
            text = match.group(3)
            transcription += text

    return transcription


def transcribe(input_file: str, is_local_whisper=False) -> str:
    if is_local_whisper:

        model_name = "large"
        command = f"./whisper.cpp/main -m whisper.cpp/models/ggml-{model_name}.bin -f {input_file} -l auto "
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        transcription = parse_transcription_csv(result.stdout)
    else:
        openai.api_key = os.environ["OPENAI_API_KEY"]
        audio_file = open(input_file, "rb")
        result = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="ja",
        )
        transcription = result["text"]
    print(transcription)
    return transcription
