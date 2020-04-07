from typing import Any
from pprint import pprint
from channel import RedisChannel


class Storage:
    def save(self, topic: str, data: Any):
        raise NotImplementedError

    def take(self, topic: str):
        raise NotImplementedError


class RedisChannelStorage(Storage):
    def __init__(self, host: str, port: int):
        self._channel = RedisChannel(host=host, port=port)

    def save(self, topic: str, data: Any):
        self._channel.push(topic, data)

    def take(self, topic: str):
        return self._channel.take(topic=topic)

    def set(self, topic: str, data: Any):
        self._channel.set(topic, data)


class MockStorage(Storage):
    def save(self, topic: str, data: Any):
        pprint(data)

    def take(self, topic: str):
        return {}
