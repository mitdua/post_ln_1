FROM python:3.12.4

WORKDIR /core

COPY requirements.txt /core/
RUN apt update && \
    apt install -y ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
ENV FLOWER_UNAUTHENTICATED_API=True
COPY /core/ /core/