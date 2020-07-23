FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 80

CMD python manage.py pyuwsgi --http 0.0.0.0:80
