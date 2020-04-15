from abc import ABC

import tornado.web
import tornado.ioloop
import json
import uuid

from models import Response
from storage import RedisChannelStorage
from common import REDIS_TARGET_TOPIC
from logger import logger
from config import spider_config


class BaseHandler(tornado.web.RequestHandler, ABC):
    def __init__(self, *args, **kwargs):
        self.storage = RedisChannelStorage(host=spider_config.REDIS_HOST,
                                           port=spider_config.REDIS_PORT,
                                           password=spider_config.REDIS_PASSWORD)
        super().__init__(*args, **kwargs)


class ProblemHandler(BaseHandler, ABC):
    def get(self):
        """
        :param key problem id
        :param oj problem origin
        :return:
        """
        params = self._get_params()
        if params is None:
            self.finish(
                json.dumps(dict(Response(code=Response.FAIL, data=None, message="key and oj param is required"))))
        else:
            params['task_id'] = uuid.uuid1().hex
            self.storage.save(REDIS_TARGET_TOPIC, json.dumps(params))
            logger.info('create crawl problem-{}-{} success'.format(params['oj'], params['key']))
            self.finish(json.dumps(dict(Response(data=params))))

    def _get_params(self):
        params = dict()
        params['key'] = self.get_argument("key", default="")
        params["oj"] = self.get_argument("oj", default="").upper()
        for k, v in params.items():
            if v is None or v is "":
                return None
        return params


class WebServer:
    def __init__(self):
        self._app = tornado.web.Application([
            (r"/api/v1/problem/namespace/key", ProblemHandler),
        ])

    def start(self, port: int = spider_config.WEB_PORT):
        logger.info('[*]web server starting.....')
        self._app.listen(port)
        logger.info('[*]web server started.....')
        tornado.ioloop.IOLoop.current().start()
