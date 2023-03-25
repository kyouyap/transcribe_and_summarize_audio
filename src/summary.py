import openai
import os
from datetime import datetime
import pandas as pd
from parse import parse_transcription_csv


openai.api_key = os.environ["OPENAI_API_KEY"]


def summary(input_text_path, output_result_path):

    model_name = "gpt-4"
    messages = []
    start_question = f"あなたは、議事録を要約して、まとめるアシスタントです。議事録のデータが届くので、適切に要約して下さい。ただし、音声認識で文字起こしをしたデータなので文字起こしに誤りがあったり（漢字などは音を読み、文字起こしの誤りがあると思われれば修正する）、どなたが発話しているか分かりにくいという問題があることを踏まえて下さい。出力のフォーマットは下記でお願いします。\n\n結論：\nconclusion\n\n要点：\n・example1\n・example2\n・example3\n要点があれば続ける\n\n要約：\n要約文章"
    df = parse_transcription_csv(input_text_path, input_text_path.replace(
        "text", "csv").replace(".txt", ".csv"))
    # start_time->end_timeの差が1秒以上あるものを抽出する。
    df = df[df['end_time'].str.split(':').apply(lambda x: int(x[0])*3600+int(x[1])*60+float(
        x[2])) - df['start_time'].str.split(':').apply(lambda x: int(x[0])*3600+int(x[1])*60+float(x[2])) > 1]

    messages.append({"role": "system", "content": start_question})
    for index, row in df.iterrows():
        messages.append(
            {"role": "user", "content": f"{row['text']}"})

    completions = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    for choice in completions.choices:
        print(choice.message.content)
        # この結果をresult/result.txtに保存する
    with open(output_result_path, mode="w") as f:
        for choice in completions.choices:
            f.write(choice.message.content)
