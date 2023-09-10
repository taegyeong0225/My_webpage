FROM python:3.8.0-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRTIEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt