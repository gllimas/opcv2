FROM tiangolo/uvicorn-gunicorn:python3.10-slim

# set work directory
RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY ./app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install Cmake
RUN pip install opencv-python-headless
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libopencv-dev \
    v4l-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install dlib




RUN pip install -r requirements.txt

COPY ./app .
