FROM python:3.8.7-buster

RUN apt-get update
RUN apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN export FLASK_APP=run.py

RUN export FLASK_CONFIG=development

RUN flask run

COPY . /app

ENTRYPOINT [ "python" ]