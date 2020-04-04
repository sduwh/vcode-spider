#!/usr/bin/env python3

import threading
from queue import Queue
from web import WebServer
from crawler import Crawlers
from models import Problem, Task
from storage import Storage, RedisChannelStorage, MockStorage

PROBLEM_TOPIC = "vcode-spider-problem"


class Dispatcher(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__(name="dispatcher", daemon=True)
        self._queue = queue

    def run(self):
        # TODO: temporary dispatch
        for namespace in ["SDUT","HDU", "POJ"]:
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
            problem: Problem = Crawlers.crawl(task.namespace, task.key)
            self._storage.save(problem.as_dict())


class Spider:
    def __init__(self, workers: int = 2):
        queue = Queue()
        # storage = RedisChannelStorage(host="127.0.0.1", port=6379, topic=PROBLEM_TOPIC)  # TODO: temporary local
        storage = MockStorage()

        self._dispatcher = Dispatcher(queue=queue)
        self._workers = []
        for _ in range(workers):
            self._workers.append(Worker(queue=queue, storage=storage))

    def start(self):
        self._dispatcher.start()
        for w in self._workers:
            w.start()

        self._dispatcher.join()
        for w in self._workers:
            w.join()


def main():
    Spider().start()


if __name__ == "__main__":
    main()
