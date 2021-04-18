FROM python:3.8.7-buster

EXPOSE 5000

RUN apt-get update
RUN apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "run.py" ]

# CMD ["python", "run.py", "run" ]