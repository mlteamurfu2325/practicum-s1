"""Module for downloading the Faster-Whisper models."""

from pathlib import Path

from faster_whisper import download_model


DIR = str(Path.cwd()) + "/models/faster-whisper/"
MODELS = ["medium", "large-v3"]

for model in MODELS:
    try:
        download_model(model, output_dir=f"{DIR}/{model}/")
    except Exception as error:
        print(f"An exception occured: {error}")

print("Done!")
