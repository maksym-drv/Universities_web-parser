FROM python:3.9.7-buster

ENV FIREFOX_VER 87.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /parser

COPY requirements.txt /parser/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["/parser/entrypoint.sh"]