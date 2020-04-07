import logging
import os

spider_config = None


class Config:
    LOG_FILE = '/tmp/vcode-spider.log'
    LOG_LEVEL = logging.INFO
    REDIS_PORT = 6379
    REDIS_HOST = '127.0.0.1'
    OJ_NAMESPACE_LIST = ['SDUT', 'HDU', 'POJ']


class ProdConfig(Config):
    LOG_FILE = '/var/log/vcode-spider/vcode-spider.log'
    LOG_LEVEL = logging.INFO


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG


if os.environ.get('ENVIRONMENT', 'prod') == 'prod':
    spider_config = ProdConfig()
else:
    spider_config = DevConfig()
