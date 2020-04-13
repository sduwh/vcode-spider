#!/usr/bin/env python3

import threading
import _thread

from queue import Queue
from web import WebServer
from crawler import Crawlers
from models import Problem, Task, Response
from storage import Storage, RedisChannelStorage
from logger import logger
from common import PROBLEM_TOPIC, TARGET_TOPIC, TARGET_RESULT_TOPIC, NAMESPACE_TOPIC
from exceptions import CrawlerException
from config import spider_config


class Dispatcher(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__(name="dispatcher", daemon=True)
        self._queue = queue

    def run(self):
        # TODO: temporary dispatch
        for namespace in spider_config.OJ_NAMESPACE_LIST:
            for n in range(1000, 2000):
                self._queue.put(Task(namespace, str(n)))


class Worker(threading.Thread):
    def __init__(self, queue: Queue, storage: Storage):
        super().__init__(name="worker", daemon=True)
        self._queue = queue
        self._storage = storage

    def run(self):
        while True:
            task: Task = self._queue.get()
            try:
                problem: Problem = Crawlers.crawl(task.namespace, task.key)
                self._storage.save(PROBLEM_TOPIC, dict(problem))
                logger.info('crawl problem-{} success'.format(problem.base_info()))
                if task.task_id is not "":
                    self._storage.save(TARGET_RESULT_TOPIC,
                                       dict(Response(code=Response.SUCCESS,
                                                     data={'task_id': task.task_id},
                                                     message='success')))
                    logger.info(
                        'task: crawl problem-{} success'.format(problem.base_info()))
            except KeyError:
                logger.error({'task_id': task.task_id, 'message': 'The task is failed, check the OJ'})
                self._storage.save(TARGET_RESULT_TOPIC,
                                   dict(Response(code=Response.FAIL,
                                                 data={'task_id': task.task_id},
                                                 message='The task is failed, check the OJ')))
            except CrawlerException as e:
                logger.error({'task_id': task.task_id, 'message': e})
                self._storage.save(TARGET_RESULT_TOPIC,
                                   dict(Response(code=Response.FAIL,
                                                 data={'task_id': task.task_id},
                                                 message='The task is failed, check the key exist')))
            except Exception as e:
                logger.exception(e)


class Consumer(threading.Thread):
    def __init__(self, queue: Queue, storage: Storage):
        super().__init__(name='consumer', daemon=True)
        self._storage = storage
        self._queue = queue

    def run(self) -> None:
        while True:
            target = self._storage.take(TARGET_TOPIC)
            self._queue.put(Task(namespace=target.get('oj'), key=target.get('key'), task_id=target.get('task_id')))


class Spider:
    def __init__(self, workers: int = 2, consumer=2):
        queue = Queue()
        storage = RedisChannelStorage(host=spider_config.REDIS_HOST,
                                      port=spider_config.REDIS_PORT,
                                      password=spider_config.REDIS_PASSWORD)
        # storage = MockStorage()
        self._storage = storage
        self._dispatcher = Dispatcher(queue=queue)
        self._workers = []
        self._consumer = []
        for _ in range(workers):
            self._workers.append(Worker(queue=queue, storage=storage))
        for _ in range(consumer):
            self._consumer.append(Consumer(queue=queue, storage=storage))

    def start(self):
        logger.info('[*]spider starting.....')
        self._storage.set(topic=NAMESPACE_TOPIC, data=",".join(spider_config.OJ_NAMESPACE_LIST))
        self._dispatcher.start()
        for w in self._workers:
            w.start()
        for c in self._consumer:
            c.start()
        logger.info('[*]spider start success.')
        self._dispatcher.join()
        for w in self._workers:
            w.join()
        for c in self._consumer:
            c.join()


def main():
    logger.info(spider_config.REDIS_PASSWORD)
    _thread.start_new_thread(Spider().start, ())
    WebServer().start()


if __name__ == "__main__":
    main()
