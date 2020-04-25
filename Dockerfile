FROM python:3.7-alpine3.10

ENV SPIDER_ENV prod

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requestments.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

ENTRYPOINT ["python3", "/app/src/main.py"]