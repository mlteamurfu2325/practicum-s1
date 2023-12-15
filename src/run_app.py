from pathlib import Path
import streamlit as st
from faster_whisper import WhisperModel


def save_uploaded_file(uploaded_file):
    # specify the directory
    dir_path = Path('media')
    dir_path.mkdir(parents=True, exist_ok=True)  # create directory if it does not exist

    # create a path object for the file
    file_path = dir_path / uploaded_file.name

    # write the file
    with file_path.open("wb") as f:
        f.write(uploaded_file.getbuffer())

    st.toast(f"Saved file: {file_path}")

    return file_path


st.markdown('### Итоговый проект группы 1.12')

uploaded_file = st.file_uploader('Загрузите файл подходящего формата',
                                 type=['mp3', 'wav', 'mp4', 'webm'])

if uploaded_file is not None:
    uploaded_file_path = save_uploaded_file(uploaded_file)

    with st.spinner('Загружаем модель. Минутку...'):
        model = WhisperModel(
                            model_size_or_path='models/large-v3/',
                            device="cpu",
                            compute_type="int8",
                            num_workers=4,
                            local_files_only=True
                            )

    with st.spinner('Первичный анализ файла. Минутку...'):
        segments, info = model.transcribe(audio=str(uploaded_file_path),
                                      beam_size=5)

    st.write(f"Язык речи: {info.language} с вероятностью {info.language_probability}")

    st.write(f"Длительность в секундах: {info.duration}")

    progress_text = 'Идёт транскрибирование сегментов аудио'
    
    segments_bar = st.progress(0, text=progress_text)
    
    for segment in segments:
        st.write("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        curr_bar_val = segment.end / info.duration
        segments_bar.progress(curr_bar_val, text=progress_text)
