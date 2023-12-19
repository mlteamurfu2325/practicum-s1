from pathlib import Path
import time
import streamlit as st
from faster_whisper import WhisperModel
from pytube import YouTube
from utils.cuda_checker import check_cuda
from transformers import pipeline


def save_uploaded_file(uploaded_file):
    """
        uploaded_file : file uploaded via streamlit.file_uploader()

        Return : str
            absolute filepath to the new uploaded file.

        Comment: save the new uploaded file into local drive and provide its filepath.
    """
    # specify the directory
    dir_path = Path('../media')
    dir_path.mkdir(parents=True, exist_ok=True)  # create directory if it does not exist

    # create a path object for the file
    file_path = dir_path / uploaded_file.name

    # write the file
    with file_path.open("wb") as f:
        f.write(uploaded_file.getbuffer())

    st.toast(f"Saved file: {file_path}")

    return file_path


st.markdown('### 📖 Итоговый проект группы 1.12')

uploaded_file_path = ''
with st.container():
    st.write('Выбор видеофайла для транскибирования')
    file_mode = st.selectbox("Выберите тип загрузки файла: ", ['Local', 'URL'], index=0,
                             help='Используйте "Local" для загрузки файла с локального компьютера или выберите "URL" для загрузки видео с YouTube.')
    if file_mode == 'Local':
        uploaded_file = st.file_uploader('🔽 Загрузите файл подходящего формата',
                                 type=['mp3', 'wav', 'mp4', 'webm'])

        if uploaded_file is not None:
            st.session_state['file_path'] = save_uploaded_file(uploaded_file)

    else:
        url = st.text_input('URL', help='Введите URL ссылку на видео с YouTube')
        chosen = st.button('Выбрать видео')
        if chosen:
            tmp_dir_path = Path('media')
            tmp_dir_path.mkdir(parents=True, exist_ok=True)
            tmp_name = url.split('?v=')[1] + '.mp4'
            uploaded_file_path = tmp_dir_path / tmp_name
            st.session_state['file_path'] = uploaded_file_path
            yt = YouTube(url)
            stream = yt.streams.get_lowest_resolution()
            with st.spinner('Загружаем видео...'):
                stream.download(output_path=tmp_dir_path, filename=tmp_name)
                st.toast(f'Видео с YouTube загружено {uploaded_file_path}')

    with st.expander('Дополнительный функционал'):
        summary_checkbox = st.checkbox('Суммаризация текста', value=False)
        transcribe_text = ""
    
    transcribe = st.button('Запустить транскибирование!')

    if transcribe:
        time_start = time.time()
        uploaded_file_path = st.session_state['file_path']

        with st.spinner('🚚 Загружаем модель. Минутку...'):
            if check_cuda():
                selected_model_path = '../models/faster-whisper/large-v3/'
                local_device = 'cuda'
                selected_compute_type = 'int8_float16'
                st.toast(body='Обнаружен GPU. Будет ускоряться!',
                        icon='🚀')
            else:
                selected_model_path = '../models/faster-whisper/medium/'
                local_device = 'cpu'
                selected_compute_type = 'int8'
                st.toast(body='Обнаружен CPU. Придётся подождать...',
                        icon='🐌')

            model = WhisperModel(
                                model_size_or_path=selected_model_path,
                                device=local_device,
                                compute_type=selected_compute_type,
                                num_workers=4,
                                local_files_only=True
                                )

        with st.spinner('🔬 Первичный анализ файла. Минутку...'):
            segments, info = model.transcribe(audio=str(uploaded_file_path),
                                              beam_size=5)

        st.write(f"Язык речи: {info.language} с вероятностью {info.language_probability}")

        st.write(f"Длительность в секундах: {info.duration}")

        progress_text = '⏳ Идёт транскрибирование сегментов аудио'

        segments_bar = st.progress(0, text=progress_text)

        with st.expander('📜 Транскрипт текста'):
            for segment in segments:
                st.write("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
                curr_bar_val = min(segment.end / info.duration, 1.0)
                segments_bar.progress(curr_bar_val, text=progress_text)
                
                if summary_checkbox:
                    transcribe_text += segment.text + " "

            time_total = time.time() - time_start

            st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: green;
                }
            </style>""",
            unsafe_allow_html=True,
                    )
        
        with st.expander('Дополнительная информация'):
            if summary_checkbox:
                summarizer = pipeline("summarization", model = "d0rj/rut5-base-summ")
                st.write("**Суммаризованный текст:**  ", summarizer(transcribe_text)[0]['summary_text'])

        with st.expander('🛠 Техническая информация'):
            st.markdown(f'*Общее время транскрипции*: {round(time_total)} с.')

