# Use Ubuntu as the base image
FROM ubuntu:20.04

# Install Python 3 and ffmpeg
RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy all Python files to the working directory
COPY *.py .

# Declare the environment variables that Railway injects at build time
ARG TG_API_ID
ARG TG_API_HASH
ARG OPENAI_API_KEY
ARG BOT_TOKEN

# Set the environment variables for the service.py file
ENV TG_API_ID=$TG_API_ID
ENV TG_API_HASH=$TG_API_HASH
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV BOT_TOKEN=$BOT_TOKEN

# Set the command to run the service.py file
CMD ["python3", "service.py"]
