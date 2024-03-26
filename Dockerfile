FROM python:3.10

RUN mkdir /delivery_bot

WORKDIR /delivery_bot

RUN pip install aiogram==2.25.1 requests

COPY . /delivery_bot/