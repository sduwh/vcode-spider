FROM python:3.7-alpine3.10

ENV SPIDER_ENV prod

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requestments.txt

ENTRYPOINT ["python3", "/app/src/main.py"]