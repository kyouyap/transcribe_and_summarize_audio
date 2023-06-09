
# Transcribe and Summarize Audio

このプログラムは、音声録音を取り込み、それを文字起こしし、要約を生成します。録音したい音声ファイルを指定するか、プログラム内で録音を行って処理することができます。
<!-- /img/sample.pngを差し込む -->
[![sample](./img/sample.png)](./img/sample.png)
## 事前準備

このプログラムを実行する前に、以下の手順に従って準備を行ってください。

1. (ローカルのwhisperを使いたい場合)https://github.com/openai/whisper.git からレポジトリをクローンします。
```bash
git clone https://github.com/openai/whisper.git
```

2. (ローカルのwhisperを使いたい場合)whisper.cppに入り、makeを実行してプロジェクトをビルドします。ただし、cppコンパイラがなければインストールしてください。
```bash
cd whisper
gcc -O3 -std=c11   -pthread -mavx -mavx2 -mfma -mf16c -fPIC -c ggml.c
g++ -O3 -std=c++11 -pthread --shared -fPIC -static-libstdc++ whisper.cpp ggml.o -o libwhisper.so
```

3. (ローカルのwhisperを使いたい場合)使用するモデルをダウンロードします。
```bash
bash ./models/download-ggml-model.sh large
```

4. portaudio をインストールします。M1 Mac の場合は以下のコマンドを実行してください。

```bash
python3 -m pip install --upgrade pip setuptools wheel

brew install portaudio --HEAD
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
```

## 使用法

1. 必要なパッケージをインストールします。
```bash
pip install -r requirements.txt
```

2. コマンドラインから次のようにプログラムを実行します。
```bash
python main.py
```
