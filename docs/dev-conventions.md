# Соглашения по стандартам разработки среди участников

## Соглашение по формату коммит-сообщений
Для текста коммит-сообщений предлагается использовать модель `Semantic Commit Messages`.
`<type>(<scope>): <subject>`
### Пример
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

## Соглашение по предназначению веток

Для релиза для показа на демо используется ветка `release-1.0.0`

## Соглашение по локальному контролю качества кода

Желательным является использование pre-commit проверок в соответствии с [.pre-commit-config.yaml](.pre-commit-config.yaml).
Необходимо установить `pre-commit`, `black`, `isort`:
```bash
pip install pre-commit pylint black isort
pre-commit install
```
Теперь перед коммитом будут осуществляться проверки.

Кроме того, желательным является использование `pylint`:
```bash
pylint . --ignore .venv --output-format=colorized --recursive=y --disable=C0103,C0209
```
Запускаем из директории с локальными файлами репозитория.

## Соглашение по автоматическому контролю качества кода на GitHub
GitHub Action [workflow-файл](.github/workflows/format-code.yml) для проверки с помощью `black` и `isort` при создании коммита
