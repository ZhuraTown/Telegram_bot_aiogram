FROM python:3.8-alpine

COPY . /Telegram_bot_aiogram/
WORKDIR /Telegram_bot_aiogram/


# RUN apt-get install -y python-pip python-dev build-essential
RUN pip install -r requirements.txt

