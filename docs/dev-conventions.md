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