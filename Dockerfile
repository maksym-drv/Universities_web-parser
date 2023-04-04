FROM python:3.9.7-buster

ENV AM_I_IN_DOCKER 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /parser

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr

COPY requirements.txt /parser/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["/parser/entrypoint.sh"]