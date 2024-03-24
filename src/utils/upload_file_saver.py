"""Module for saving uploaded files to disk."""

from pathlib import Path

import streamlit as st


def save_uploaded_file(uploaded_file: st.uploaded_file_manager.UploadedFile) -> Path:
    """
    Save an uploaded file to the specified directory and return the file path.

    Args:
        uploaded_file: The file uploaded by the user through the Streamlit interface.

    Returns:
        Path: The path to the saved file.
    """
    dir_path = Path("../media")
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / uploaded_file.name

    with file_path.open("wb") as f:
        f.write(uploaded_file.getbuffer())

    st.toast(f"Saved file: {file_path}")

    return file_path
