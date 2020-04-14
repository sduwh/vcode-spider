from typing import Any
from pprint import pprint
from channel import RedisChannel


class Storage:
    def save(self, topic: str, data: Any):
        raise NotImplementedError

    def take(self, topic: str):
        raise NotImplementedError


class RedisChannelStorage(Storage):
    def __init__(self, host: str, port: int, password: str):
        self._channel = RedisChannel(host=host, port=port, password=password)

    def save(self, topic: str, data: Any):
        self._channel.push(topic, data)

    def take(self, topic: str, timeout=0):
        return self._channel.take(topic=topic, timeout=timeout)

    def set(self, topic: str, data: Any):
        self._channel.set(topic, data)

    def lock(self, lock_key) -> None:
        self._channel.lock(lock_key)

    def isLock(self, lock_key) -> bool:
        return self._channel.isLock(lock_key)


class MockStorage(Storage):
    def save(self, topic: str, data: Any):
        pprint(data)

    def take(self, topic: str):
        return {}
