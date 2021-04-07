FROM python:3.7-alpine
MAINTAINER nvo87

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client \
    && apk add --update --no-cache --virtual .tmp-build-deps \
    && apk add gcc libc-dev linux-headers postgresql-dev python3-dev jpeg-dev zlib-dev \
    && pip install -r /requirements.txt \
    && apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./crm /app

RUN adduser -D user
USER user
