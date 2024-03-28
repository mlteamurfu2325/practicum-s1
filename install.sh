#!/bin/bash

# Function to prompt user for input
prompt_user() {
    local message=$1
    local default_value=$2
    read -p "$message" user_input
    if [ -z "$user_input" ]; then
        echo "$default_value"
    else
        echo "$user_input"
    fi
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to clean up on script termination or error
cleanup() {
    echo "Cleaning up..."
    deactivate >/dev/null 2>&1
    exit 1
}

# Trap signals and errors
trap cleanup SIGTERM ERR

# Check if Python and pip are available
if command_exists python3; then
    python_cmd="python3"
elif command_exists python; then
    python_cmd="python"
else
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

if command_exists pip3; then
    pip_cmd="pip3"
elif command_exists pip; then
    pip_cmd="pip"
else
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if dir_name is provided as a parameter
if [ -z "$1" ] || [[ "$1" != --dir_name=* ]]; then
    dir_name=$(prompt_user "Enter the directory name: ")
else
    dir_name=$(echo "$1" | cut -d'=' -f2)
fi

# Check if git_branch is provided as a parameter
if [ -z "$2" ] || [[ "$2" != --git_branch=* ]]; then
    branch=$(prompt_user "Enter the git branch (press Enter for 'main'): " "main")
else
    branch=$(echo "$2" | cut -d'=' -f2)
fi

# Check if llm_summarizer is provided as a parameter
if [ -z "$3" ] || [[ "$3" != --llm_summarizer=* ]]; then
    llm_summarizer=$(prompt_user "Do you need LLM summarizer functionality? (y/n): " "n")
else
    llm_summarizer=$(echo "$3" | cut -d'=' -f2)
fi

# Check if run_app is provided as a parameter
if [ -z "$4" ] || [[ "$4" != --run_app=* ]]; then
    run_app=$(prompt_user "Do you want to run the app? (y/n): " "n")
else
    run_app=$(echo "$4" | cut -d'=' -f2)
fi

# Create directory and navigate to it
mkdir -p "$HOME/$dir_name" && cd "$HOME/$dir_name" || exit 1

# Clone the repository with the specified branch
git clone --branch "$branch" https://github.com/mlteamurfu2325/practicum-s1.git . || exit 1

# Create virtual environment
"$python_cmd" -m venv .venv-practicum || exit 1

# Check if virtual environment exists before activating
if [ ! -d ".venv-practicum" ]; then
    echo "Virtual environment creation failed. Exiting."
    exit 1
fi

# Activate virtual environment
source .venv-practicum/bin/activate || exit 1

# Install dependencies
"$pip_cmd" install faster-whisper streamlit pytube openai pysubs2 streamlit_ext streamlit_extras || exit 1

# Create models directory
mkdir -p models/faster-whisper/ || exit 1

# Download Faster Whisper models
"$python_cmd" deploy/download_faster_whisper_models.py || exit 1

# Navigate to the src directory
cd src/ || exit 1

if [[ $llm_summarizer =~ ^[Yy]$ ]]; then
    # Check if LLM_API_KEY and LLM_URL are provided as parameters
    if [ -z "$5" ] || [[ "$5" != --llm_api_key=* ]]; then
        LLM_API_KEY=$(prompt_user "Enter the LLM API key: ")
    else
        LLM_API_KEY=$(echo "$5" | cut -d'=' -f2)
    fi

    if [ -z "$6" ] || [[ "$6" != --llm_url=* ]]; then
        LLM_URL=$(prompt_user "Enter the LLM URL: ")
    else
        LLM_URL=$(echo "$6" | cut -d'=' -f2)
    fi

    export LLM_API_KEY
    export LLM_URL
fi

if [[ $run_app =~ ^[Yy]$ ]]; then
    streamlit run run_app.py
    # Clean up on normal script completion
    cleanup
else
    # Clean up if user chooses not to run the app
    cleanup
fi
