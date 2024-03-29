FROM ubuntu:latest

LABEL org.opencontainers.image.source https://github.com/mlteamurfu2325/practicum-s1

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl git python3 python3-pip python3-venv

# Set the working directory
WORKDIR /app

# Copy the installation script to the working directory
RUN curl -Ls https://raw.githubusercontent.com/mlteamurfu2325/practicum-s1/main/install.sh -o install.sh

# Make the installation script executable
RUN chmod +x install.sh

# Set default values for the script arguments
ENV DIR_NAME=practicum
ENV GIT_BRANCH=main
ENV LLM_SUMMARIZER=n
ENV RUN_APP=n

# Run the installation script with the provided arguments
RUN ./install.sh --dir_name=$DIR_NAME --git_branch=$GIT_BRANCH --llm_summarizer=$LLM_SUMMARIZER --run_app=$RUN_APP

# Set the default command to run when the container starts
CMD ["/bin/bash", "-c", "source /root/practicum/.venv-practicum/bin/activate && cd /root/practicum/src && streamlit run run_app.py"]
