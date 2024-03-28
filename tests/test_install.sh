#!/bin/bash

# Test setup function
oneTimeSetUp() {
    # Set up any necessary test environment or variables
    export HOME=/tmp
    rm -rf "$HOME/test_dir"
    ./install.sh --dir_name=test_dir --git_branch=main --llm_summarizer=n --run_app=n
}

# Test teardown function
oneTimeTearDown() {
    # Clean up any test artifacts or temporary files
    rm -rf "$HOME/test_dir"
    unset HOME
}

# Test case for Whisper models download
test_whisper_models_downloaded() {
    # Test case 1: large-v3 model downloaded
    assertTrue "[ -f \"$HOME/test_dir/models/faster-whisper/large-v3/model.bin\" ]"
    # Test case 2: medium model downloaded
    assertTrue "[ -f \"$HOME/test_dir/models/faster-whisper/medium/model.bin\" ]"
}

# Test case for Python virtualenv creation
test_virtualenv_creation() {
    # Test case 3: virtualenv dir created
    assertTrue "[ -d \"$HOME/test_dir/.venv-practicum/\" ]"
}

# Test case for main program files installed
test_whisper_models_downloaded() {
    # Test case 4: summ_fetcher.py
    assertTrue "[ -f \"$HOME/test_dir/src/llm_summ/summ_fetcher.py\" ]"
    # Test case 5: run_app.py
    assertTrue "[ -f \"$HOME/test_dir/src/run_app.py\" ]"
    # Test case 6: cuda_checker.py
    assertTrue "[ -f \"$HOME/test_dir/src/utils/cuda_checker.py\" ]"
    # Test case 7: data_validator.py
    assertTrue "[ -f \"$HOME/test_dir/src/utils/data_validator.py\" ]"
    # Test case 8: upload_file_saver.py
    assertTrue "[ -f \"$HOME/test_dir/src/utils/upload_file_saver.py\" ]"
}

# Run shunit2 tests
. shunit2
