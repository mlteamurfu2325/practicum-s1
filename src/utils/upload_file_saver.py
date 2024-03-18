"""Module for saving uploaded files to disk."""

from pathlib import Path

import streamlit as st


# No type hints yet available for Streamlit
# so no specifi type hint available for `uploaded_file`
# See https://github.com/streamlit/streamlit/issues/7801
def save_uploaded_file(uploaded_file) -> Path:
    """
    Save an uploaded file to the specified directory and return the file path.

    :param uploaded_file: The file uploaded by the user through the Streamlit interface.
    :return: The path to the saved file.
    :rtype: Path
    """
    dir_path = Path("../media")
    dir_path.mkdir(parents=True, exist_ok=True)

    # create a path object for the file
    file_path = dir_path / uploaded_file.name

    # write the file
    with file_path.open("wb") as f:
        f.write(uploaded_file.getbuffer())

    st.toast(f"Saved file: {file_path}")

    return file_path
