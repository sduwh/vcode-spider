#!/usr/bin/env python3

import threading
import _thread

from queue import Queue
from web import WebServer
from crawler import Crawlers
from models import Problem, Task, Response
from storage import Storage, RedisChannelStorage

from common import PROBLEM_TOPIC, TARGET_TOPIC, TARGET_RESULT_TOPIC
from exceptions import CrawlerException


class Dispatcher(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__(name="dispatcher", daemon=True)
        self._queue = queue

    def run(self):
        # TODO: temporary dispatch
        for namespace in ["SDUT", "HDU", "POJ"]:
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
                if task.task_id is not "":
                    self._storage.save(TARGET_RESULT_TOPIC,
                                       dict(Response(code=Response.SUCCESS,
                                                     data={'task_id': task.task_id},
                                                     message='success')))
            except (KeyError, CrawlerException):
                self._storage.save(TARGET_RESULT_TOPIC,
                                   dict(Response(code=Response.FAIL,
                                                 data={'task_id': task.task_id},
                                                 message='The task is failed, check the OJ and KEY')))


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
        storage = RedisChannelStorage(host="127.0.0.1", port=6379)
        # storage = MockStorage()

        self._dispatcher = Dispatcher(queue=queue)
        self._workers = []
        self._consumer = []
        for _ in range(workers):
            self._workers.append(Worker(queue=queue, storage=storage))
        for _ in range(consumer):
            self._consumer.append(Consumer(queue=queue, storage=storage))

    def start(self):
        self._dispatcher.start()
        for w in self._workers:
            w.start()
        for c in self._consumer:
            c.start()

        self._dispatcher.join()
        for w in self._workers:
            w.join()
        for c in self._consumer:
            c.join()


def main():
    _thread.start_new_thread(Spider().start, ())
    WebServer().start()


if __name__ == "__main__":
    main()
