# Инструкция по развёртыванию
На примере Ubuntu/Debian:

```sh
apt update && apt upgrade -y

apt install python3 python3-virtualenv python3-pip

mkdir $HOME/fin-proj && cd $HOME/fin-proj

git clone https://github.com/mlteamurfu2325/practicum-s1.git .

python3 -m virtualenv .venv

source .venv/bin/activate

pip install faster-whisper streamlit

mkdir models

python3 utils/download_models.py

python3 src/run_app.py
```
