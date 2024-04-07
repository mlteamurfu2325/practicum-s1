import time
from pathlib import Path
from typing import Dict

import pysubs2
import streamlit as st
import streamlit_ext as ste
from faster_whisper import WhisperModel
from pytube import YouTube
from streamlit_extras.stylable_container import stylable_container

from llm_summ.summ_fetcher import fetch_summary
from utils.cuda_checker import check_cuda
from utils.data_validator import validate_youtube_url
from utils.upload_file_saver import save_uploaded_file


st.set_page_config(
    page_title="Транскрайбер-аннотатор",
    page_icon="🎙️",
)

st.markdown("### 📖 Итоговый проект группы 1.12")

uploaded_file_path = ""
with st.container():
    st.write("Выбор медиафайла для транскрибирования")
    file_mode = st.selectbox(
        "Выберите тип загрузки файла: ",
        ["С Вашего устройства", "С YouTube"],
        index=0,
        help="С Вашего устройства - для загрузки Вашего файла или С YouTube - для загрузки видео по ссылке с YouTube.",
    )
    if file_mode == "С Вашего устройства":
        uploaded_file = st.file_uploader(
            label="🔽 Загрузите файл подходящего формата",
            type=["mp3", "wav", "mp4", "webm"],
            accept_multiple_files=False,
        )

        if uploaded_file is not None:
            st.session_state["file_path"] = save_uploaded_file(uploaded_file)

    else:
        url = st.text_input(
            label="Ссылка на YouTube",
            placeholder="Ссылка формата https://www.youtube.com/watch?v=...",
            key="yt_url_input",
        )
        if not validate_youtube_url(url):
            need_url_message = (
                "🙃 Я исчезну, когда Вы введёте корректную ссылку на YouTube."
                + "После ввода нажмите Enter или кликните/тапните "
                + "по любому пустому месту на экране"
            )
            st.info(need_url_message)

        else:
            chosen = st.button("📺 Скачать файл с YouTube")
            if chosen:
                tmp_dir_path = Path("../media")
                tmp_dir_path.mkdir(parents=True, exist_ok=True)
                tmp_name = url.split("?v=")[1] + ".mp4"
                uploaded_file_path = tmp_dir_path / tmp_name
                st.session_state["file_path"] = uploaded_file_path
                try:
                    yt = YouTube(url)
                    stream = yt.streams.get_audio_only()
                    with st.spinner("📥 Загружаем файл..."):
                        stream.download(output_path=tmp_dir_path, filename=tmp_name)
                        st.toast(f"💯 Файл с YouTube загружен {uploaded_file_path}")
                except Exception:
                    st.error(
                        "😔 Не удалось загрузить видео с YouTube. Попробуйте иную ссылку или загрузите файл с устройства"
                    )

    with st.expander("🗃️ Дополнительный функционал"):
        summary_checkbox = st.checkbox("🔎 Аннотирование текста", value=False)
        transcribe_text = ""

        if summary_checkbox:
            model_options: Dict[str, str] = {
                "google/gemma-7b-it:nitro": "Gemma 7B (nitro) [платно]",
                "google/gemma-7b-it:free": "Gemma 7B [бесплатно]",
                "google/gemini-pro": "Gemini Pro 1.0 [платно]",
                "openai/gpt-4-turbo-preview": "GPT 4 Turbo Preview [платно]",
            }

            selected_model = st.selectbox(
                "Выберите модель LLM для аннотирования:",
                options=list(model_options.keys()),
                format_func=lambda x: model_options[x],
            )

    transcribe = st.button(
        label="🏁 Запустить транскрибирование!",
        disabled=not st.session_state.get("file_path"),
    )

    if transcribe:
        time_start = time.time()
        uploaded_file_path = st.session_state["file_path"]

        with st.spinner("🚚 Загружаем модель. Минутку..."):
            if check_cuda():
                selected_model_path = "../models/faster-whisper/large-v2/"
                local_device = "cuda"
                selected_compute_type = "int8_float16"
                st.toast(body="Обнаружен GPU. Будет ускоряться!", icon="🚀")
            else:
                selected_model_path = "../models/faster-whisper/medium/"
                local_device = "cpu"
                selected_compute_type = "int8"
                st.toast(body="Обнаружен CPU. Придётся подождать...", icon="🐌")

            model = WhisperModel(
                model_size_or_path=selected_model_path,
                device=local_device,
                compute_type=selected_compute_type,
                num_workers=4,
                local_files_only=True,
            )

        with st.spinner("🔬 Первичный анализ файла. Минутку..."):
            segments, info = model.transcribe(
                audio=str(uploaded_file_path), beam_size=5
            )

        st.write(
            f"🌍 Язык речи: {info.language.upper()} с вероятностью {round(info.language_probability,2)}"
        )

        st.write(f"🕒 Длительность в секундах: {round(info.duration, 2)}")

        progress_text = "⏳ Идёт транскрибирование сегментов аудио"

        segments_bar = st.progress(0, text=progress_text)

        with st.expander("📜 Транскрипт текста"):
            transcr_text = ""
            segments_for_srt = []
            for segment in segments:
                st.write(
                    "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
                )
                transcr_text += segment.text + " "
                segment_dict = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                }
                segments_for_srt.append(segment_dict)
                curr_bar_val = min(segment.end / info.duration, 1.0)
                segments_bar.progress(curr_bar_val, text=progress_text)

                if summary_checkbox:
                    transcribe_text += segment.text + " "

            time_total = time.time() - time_start

            # change progress bar color when done
            st.markdown(
                """
            <style>
                .stProgress > div > div > div > div {
                    background-color: green;
                }
            </style>""",
                unsafe_allow_html=True,
            )

        with st.expander("📖 Текст без временны́х меток:"):
            # wrap text to fit in the container with copy-to-clipboard
            with stylable_container(
                "codeblock",
                """
                code {
                    white-space: pre-wrap !important;
                }
                """,
            ):
                st.code(body=transcr_text, language=None)

        with st.expander("🔎 Аннотированный текст"):
            if summary_checkbox:
                with st.spinner("🕵️‍♂️ Аннотируем текст..."):
                    summarized_text = fetch_summary(
                        text=transcr_text, llm_model=selected_model
                    )
                    with stylable_container(
                        "codeblock",
                        """
                        code {
                            white-space: pre-wrap !important;
                        }
                        """,
                    ):
                        st.code(body=summarized_text, language=None)

        with st.expander("🎞️ SRT-файл для скачивания"):
            subs = pysubs2.load_from_whisper(segments_for_srt)
            srt_fine_name = f"{Path(uploaded_file_path).name}.srt"
            srt_file_path = f"../media/{srt_fine_name}"
            subs.save(srt_file_path)
            with open(srt_file_path) as f:
                ste.download_button("📎 Скачать SRT", f, file_name=srt_fine_name)

        with st.expander("🛠 Техническая информация"):
            st.markdown(f"*Общее время транскрипции*: {round(time_total)} с.")
