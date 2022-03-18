FROM python:3-slim

RUN apt-get update -qq && \
    apt-get install -y unixodbc unixodbc-dev libpq-dev

COPY . /app
WORKDIR /app

RUN ["pip3", "install", "-r", "requirements.txt"]

CMD ["python3", "worker.py"]
