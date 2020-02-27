from typing import Any
from pprint import pprint
from channel import RedisChannel


class Storage:
    def save(self, data: Any):
        raise NotImplementedError


class RedisChannelStorage(Storage):
    def __init__(self, host: str, port: int, topic: str):
        self._channel = RedisChannel(host=host, port=port)
        self._topic = topic

    def save(self, data: Any):
        self._channel.push(self._topic, data)


class MockStorage(Storage):
    def save(self, data: Any):
        pprint(data)
