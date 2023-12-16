# Соглашение по формату коммит-сообщений
Для текста коммит-сообщений предлагается использовать модель `Semantic Commit Messages`.
`<type>(<scope>): <subject>`
## Пример
```
feat(summ): add summarizer model 
^---------^  ^------------------^
|                  |
|                  +-> Кратко, в настоящем времени.
|
+-------> Тип - chore, docs, feat, fix, refactor, style, test, perf, ci, revert, deployment.
          И скоуп (сфера) изменений
```
Примерный список скоупов:
* core - основная функциональность по запуску streamlit
* summ - модель саммаризации текста
* transcr - транскрайбер `faster-whisper`
* utils - вспомогательные утилиты
* ...

Примеры оформления из истории нашего репозитория:

`docs(deployment): add draft deployment info`

`feat(utils): add faster-whisper models downloader`

`feat(core): add first prototype`


# Инструкция по развёртыванию
На примере Ubuntu/Debian:

```sh
apt update && apt upgrade -y

apt install python3 python3-virtualenv python3-pip git

mkdir $HOME/fin-proj && cd $HOME/fin-proj

git clone https://github.com/mlteamurfu2325/practicum-s1.git .

python3 -m virtualenv .venv

source .venv/bin/activate

pip install faster-whisper streamlit

mkdir models

python3 utils/download_models.py

python3 src/run_app.py
```
