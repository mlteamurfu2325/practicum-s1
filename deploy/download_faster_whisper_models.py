"""Module for downloading the Faster-Whisper models."""

import os
from pathlib import Path

from faster_whisper import download_model


DIR = os.path.join(str(Path.cwd()), "models", "faster-whisper")
MODELS = ["medium", "large-v2"]


def download_models():
    for model in MODELS:
        try:
            download_model(model, output_dir=os.path.join(DIR, model))
        except Exception as err:
            print(f"An exception occured while downloading model {model}: {err}")
        print("Model download!")


if __name__ == "__main__":
    download_models()
