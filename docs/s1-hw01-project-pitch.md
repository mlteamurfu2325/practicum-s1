# 📼 🤖 📜 Проект "Генерирование транскрипта (субтитров) для образовательного аудио- и видеоконтента"
## Тип задачи - "Персональный помощник для студентов" 🧑‍🎓

## 🌒 1. Введение
Данный проект предлагает пользователям (студентам) получить текстовую версию видеолекции или аудио-файла (транскрипт/субтитры). 
С помощью нашего приложения студенту будет легче ориентироваться в своих видеолекциях, а текстовый формат лекции поможет в подготовке к экзаменам.
Проект также реализует цели обеспечения цифровой доступной среды в обучении для слабослышащих и не-слышащих студентов.  

## 🔬 2. Анализ проблемы
В настоящее время очень много обучающего контента для студентов представлено в формате видеолекций.
В бесконечном потоке видео, студенту становится сложно найти нужную ему информацию. 
В связи с этим часть знаний может быть потеряна, а также потрачено большое количество времени на поиск полезной информации.
Существующие решения на популярных видеохостингах не ко всем видео предоставляют субтитры. А некоторые видеохостинги вообще не предоставляют такой возможности.
Особенно актуально всё это студентов с проблемами восприятия звуковой информации.

## 🗒️ 3. Описание решения
IT-решение будет выполнено в виде web-приложения, в которое нужно загрузить ссылку с видео/аудио-файлом (или само видео/аудио с локального устройства), и приложение выдаст текстовую версию данного видео.

Данный проект будет состоять из следующих этапов:
1) Разработка дизайна и фронтенда веб-приложения;
2) Реализация получения аудио из видео с использованием необходимых библиотек;
3) Подготовка и настройка модели машинного обучения по переводу аудио в текст (speech-to-text);
4) Реализация бекенда приложения;
5) Развертывание приложения на хостинге или облаке;
6) Тестирование.

Задачи распределяются в соответствии с профилем участника команды, указанным в разделе 5.

Предполагаемые на данном этапе технологии, инструменты, алгоритмы:
`Python`, `ffmpeg`, `Whisper`, `Streamlit`

## 🧰 4. Практическая ценность и применимость
Данное решение поможет студентам в формировании конспектов видеолекций, улучшит навигацию по видеолекциям и ускорит поиск полезной информации в видео. 
Благодаря нашему приложению, студент сможет по текстовой версии лекции оценить значимость и полезность для него конкретной видеолекции. Это позволит воспринимать бóльший и более релевантный (для конкретного студента) объем информации, что в конечно итоге улучшит качество образования в целом.

## 👷 5. Команда и план действий
Команда состоит из 4-х человек (группа №12):  
Кирилл Хитрин - Тимлид, менеджер проекта  
Алексей Горбачев - UI/UX-проектировщик, фронтенд-разработчик  
Данил Хардин - Инженер по машинному обучению, разработчик бэкенда  
Елена Икрина - QA-инженер, технический писатель

В процентном отношении этапы имеют следующее ресурсно-временное распределение:
1) Разработка дизайна и фронтенда веб-приложения - 15%;
2) Реализация получения аудио из видео с использованием необходимых библиоте - 20%;
3) Подготовка и настройка модели машинного обучения по переводу аудио в текст (speech-to-text) - 20%;
4) Реализация бекенда приложения - 20%;
5) Развертывание приложения на хостинге или облаке - 10%;
6) Тестирование - 15%.

## 🎓 6. Заключение
Преимущества предлагаемого нами решения:
* использование open source технологических решений, что снижает барьеры использования программного продукта и его разработки;
* возможность локального развёртывания конечным пользователем на аппаратных платформах потребительского уровня;
* использование state-of-the-art ML-решений и моделей (локальная модель Whisper, разработанная лидером индустрии - компанией OpenAI).

В итоге будет разработан MVP (минимально жизнеспособный продукт) - IT-решение конкретной проблемы в образовательном процессе.
В реализованном виде он уже может использоваться студентами для повышения эффективности своего обучения.
Потенциально для данного решения есть возможность расширения:
1) получение транскриптов иностранных лекций с автоматическим переводом на русский язык;
2) получение выжимки по лекции с использованием локальной ML-модели или через API LLM-модели из облака.