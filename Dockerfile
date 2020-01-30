FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/meteoroid/
WORKDIR /opt/meteoroid/

RUN mkdir -p /var/log/meteoroid/

COPY Pipfile Pipfile.lock /opt/meteoroid/
RUN pip install pipenv && pipenv install --system

COPY . /opt/meteoroid/

EXPOSE 3000
