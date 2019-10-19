FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/meteoroid/
WORKDIR /opt/meteoroid/

COPY Pipfile Pipfile.lock /opt/meteoroid/
RUN pip install pipenv && pipenv install --system

COPY . /opt/meteoroid/

RUN python meteoroid/manage.py migrate

EXPOSE 8000

ENTRYPOINT ["python"]

CMD ["meteoroid/manage.py", "runserver", "0.0.0.0:8000"]

