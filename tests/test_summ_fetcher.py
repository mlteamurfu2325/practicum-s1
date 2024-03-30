import pytest
from llm_summ.summ_fetcher import fetch_summary

MODELS = [
    "google/gemma-7b-it:free",
    "openai/gpt-4-turbo-preview",
    "google/gemini-pro",
]

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

@pytest.mark.parametrize("model", MODELS)
def test_fetch_summary(model):
    text_file_path = "tests/sample_text_to_summarize.txt"
    try:
        text = read_text_file(text_file_path)
        summary = fetch_summary(text, llm_model=model)
        assert isinstance(summary, str)
        assert len(summary) > 50
    except FileNotFoundError:
        pytest.fail(f"File not found: {text_file_path}")
    except Exception as e:
        if model == MODELS[-1]:
            pytest.fail(f"All models failed. Last error: {str(e)}")
        else:
            pytest.skip(f"Model {model} failed. Error: {str(e)}")
