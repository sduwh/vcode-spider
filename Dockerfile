FROM python:3.7-alpine3.10

ENV SPIDER_ENV prod

COPY . /app

WORKDIR /app

RUN pip install -r /app/requestments.txt && mkdir -p /log/vcode-spider

ENTRYPOINT ["python3", "/app/src/main.py"]