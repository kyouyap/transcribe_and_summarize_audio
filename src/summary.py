import openai
import os


def summary(transcription,model_name="gpt-3.5-turbo"):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    model_name = "gpt-3.5-turbo"
    messages = []
    start_question = "あなたは、議事録を要約して、まとめるアシスタントです。議事録のデータが届くので、適切に要約して下さい。出力のフォーマットは下記でお願いします。"

    start_question += """
# 議事録

## 議題1: タイトル1

### 内容
- 点1
- 点2
- 点3

### 決定事項
- 決定1
- 決定2

### 議論の要約
- 内容

## 議題2: タイトル1

### 内容
- 点1
- 点2
- 点3

### 決定事項
- 決定1
- 決定2

### 議論の要約
- 内容

以下議題の数だけ繰り返す
    """
    messages.append({"role": "system", "content": start_question})

    messages.append(
        {"role": "user", "content": f"{transcription}"})

    completions = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    text = ""
    for choice in completions.choices:
        print(choice.message.content)
        text += choice.message.content+"\n"  # noqa
    return text
