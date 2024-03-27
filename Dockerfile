# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install git
RUN apt-get update && apt-get install -y git

# Install the project dependencies
RUN pip install faster-whisper streamlit pytube openai pysubs2 streamlit_ext streamlit_extras

# Create models directory
RUN mkdir -p models/faster-whisper/

# Download Faster Whisper models
RUN python deploy/download_faster_whisper_models.py

# Set environment variables for LLM summarizer functionality (if needed)
# ENV LLM_API_KEY=your_api_key
# ENV LLM_URL=your_url

# Expose the Streamlit port
EXPOSE 8501

# Set the entrypoint command to run the Streamlit app
CMD ["streamlit", "run", "src/run_app.py"]
