FROM python:3.7-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

USER root

COPY . /app

RUN apt-get update && \
    apt-get install -y apt-utils gcc python3-dev git unzip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH /app

ENTRYPOINT ["python"]

CMD ["run.py"]
