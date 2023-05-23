FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt
COPY Games /Games
WORKDIR /Games
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password games-user

USER games-user