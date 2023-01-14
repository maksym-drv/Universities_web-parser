FROM python:3.9.7-buster

ENV FIREFOX_VER 87.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /parser

COPY requirements.txt /parser/

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

COPY ./entrypoint.sh .

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["/parser/entrypoint.sh"]