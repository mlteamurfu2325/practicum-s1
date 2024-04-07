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
cleanup_on_ok() {
    echo "Cleaning up..."
    deactivate >/dev/null 2>&1
    exit 0
}

cleanup_on_not_ok() {
    echo "Cleaning up..."
    deactivate >/dev/null 2>&1
    exit 1
}

# Trap signals and errors
trap cleanup_on_not_ok SIGTERM ERR

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

# Parse command line arguments
for arg in "$@"; do
    case $arg in
        --dir_name=*)
            dir_name="${arg#*=}"
            ;;
        --git_branch=*)
            branch="${arg#*=}"
            ;;
        --llm_summarizer=*)
            llm_summarizer="${arg#*=}"
            ;;
        --run_app=*)
            run_app="${arg#*=}"
            ;;
        --llm_api_key=*)
            LLM_API_KEY="${arg#*=}"
            ;;
        --llm_url=*)
            LLM_URL="${arg#*=}"
            ;;
    esac
done

# Set default values if not provided
dir_name=${dir_name:-$(prompt_user "Enter the new directory name in your $HOME: ")}
branch=${branch:-$(prompt_user "Enter the git branch (press Enter for 'main'): " "main")}
llm_summarizer=${llm_summarizer:-$(prompt_user "Do you need LLM summarizer functionality? (y/n): " "n")}
run_app=${run_app:-$(prompt_user "Do you want to run the app? (y/n): " "n")}

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
"$pip_cmd" install -r requirements.txt || exit 1

# Create models directory
mkdir -p models/faster-whisper/ || exit 1

# Download Faster Whisper models
"$python_cmd" deploy/download_faster_whisper_models.py || exit 1

# Navigate to the src directory
cd src/ || exit 1

if [[ $llm_summarizer =~ ^[Yy]$ ]]; then
    # Check if LLM_API_KEY and LLM_URL are provided as parameters
    if [ -z "$LLM_API_KEY" ]; then
        LLM_API_KEY=$(prompt_user "Enter the LLM API key: ")
    fi

    if [ -z "$LLM_URL" ]; then
        LLM_URL=$(prompt_user "Enter the LLM URL: ")
    fi

    export LLM_API_KEY
    export LLM_URL
fi

if [[ $run_app =~ ^[Yy]$ ]]; then
    streamlit run run_app.py
    # Clean up on normal script completion
    cleanup_on_ok
else
    # Clean up if user chooses not to run the app
    cleanup_on_ok
fi
