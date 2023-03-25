
# Transcribe and Summarize Audio

このプログラムは、音声録音を取り込み、それを文字起こしし、要約を生成します。録音したい音声ファイルを指定するか、プログラム内で録音を行って処理することができます。

## 事前準備

このプログラムを実行する前に、以下の手順に従って準備を行ってください。

1. https://github.com/openai/whisper.git からレポジトリをクローンします。
```bash
git clone https://github.com/openai/whisper.git
```

2. whisper.cppに入り、makeを実行してプロジェクトをビルドします。ただし、cppコンパイラがなければインストールしてください。
```bash
cd whisper
gcc -O3 -std=c11   -pthread -mavx -mavx2 -mfma -mf16c -fPIC -c ggml.c
g++ -O3 -std=c++11 -pthread --shared -fPIC -static-libstdc++ whisper.cpp ggml.o -o libwhisper.so
```

3. 使用するモデルをダウンロードします。`{model_name}` には使用するモデル名を入力してください。
```bash
bash ./models/download-ggml-model.sh {model_name}
```

4. portaudio をインストールします。M1 Mac の場合は以下のコマンドを実行してください。

```bash
python3 -m pip install --upgrade pip setuptools wheel

brew install portaudio --HEAD
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
```

5. OPENAI_API_KEY 環境変数に OpenAI API キーを設定します。
```bash
export OPENAI_API_KEY='your_api_key_here'
```

## 使用法

1. 必要なパッケージをインストールします。
```bash
pip install -r requirements.txt
```

2. コマンドラインから次のようにプログラムを実行します。
```bash
python main.py [-i INPUT_FILE] [-m MODEL_NAME] [-t TEXT_FILE]
```
- `-i` または `--input`: 音声ファイルを指定します。指定しない場合、プログラム内で録音が開始されます。
- `-m` または `--model`: 使用するモデル名を指定します。初期値は "base" です。
- `-t` または `--text`: 文字起こしされたテキストファイルを指定します。指定しない場合、新たに作成します。

### 使用例

#### 既存の音声ファイルを処理する場合

```bash
python main.py -i audio/existing_audio.wav -m base
```

#### 新規録音を行い、処理する場合

```bash
python main.py -m base
```

プログラム内で録音が開始されます。録音を終了するには `q` キーを押してください。録音された音声は処理され、テキストファイルが生成されます。