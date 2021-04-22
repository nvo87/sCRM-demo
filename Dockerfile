FROM python:3.8.8-alpine
MAINTAINER nvo87

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client \
    && apk add --update --no-cache --virtual .tmp-build-deps \
    && apk add gcc libc-dev linux-headers postgresql-dev python3-dev jpeg-dev zlib-dev \
    && apk add libffi-dev openssl-dev rust cargo \
    && apk del .tmp-build-deps

RUN addgroup workers \
    && adduser -D worker workers

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /worker/app
RUN mkdir -p /worker/reports

COPY ./.pylintrc /worker/.pylintrc
COPY ./setup.cfg /worker/setup.cfg

RUN chown worker:workers -R /worker

USER worker
WORKDIR /worker/app
