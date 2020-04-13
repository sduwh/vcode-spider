import logging
import os

spider_config = None


class Config:
    LOG_FILE = '/tmp/vcode-spider.log'
    LOG_LEVEL = logging.INFO
    REDIS_PORT = 6379
    REDIS_HOST = '127.0.0.1'
    REDIS_PASSWORD = None
    OJ_NAMESPACE_LIST = ['SDUT', 'HDU', 'POJ']
    WEB_PORT = 8000


class ProdConfig(Config):
    LOG_FILE = '/log/vcode-spider/vcode-spider.log'
    LOG_LEVEL = logging.INFO
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_HOST = os.environ.get('REDIS_HOST', 'vcode-redis')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
    WEB_PORT = 80


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG
    WEB_PORT = 8081


if os.environ.get('SPIDER_ENV', 'prod') == 'prod':
    spider_config = ProdConfig()
else:
    spider_config = DevConfig()
