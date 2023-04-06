# 仮想環境を作成する
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# portaudioを入れる
# osによってインストール方法を変える

if [ "$(uname)" == 'Darwin' ]; then
    brew install portaudio
elif [ "$(expr substr $(uname -s) 1 5)" == 'Linux' ]; then
    sudo apt-get install -y portaudio19-dev
fi