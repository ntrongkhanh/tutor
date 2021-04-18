FROM python:3.8.7-buster

EXPOSE 5000

RUN apt-get update
RUN apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "bash","run.sh" ]

# CMD ["python", "run.py", "run" ]