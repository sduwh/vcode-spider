import json
from typing import Any
from redis import Redis


class ChannelListener:
    def on_next(self, message: Any):
        raise NotImplementedError

    def on_exception(self, e: Exception):
        raise NotImplementedError

    def on_complete(self):
        raise NotImplementedError


class Channel:
    def push(self, topic: str, message: Any):
        raise NotImplementedError

    def take(self, topic: str, timeout: int) -> Any:
        raise NotImplementedError

    def listen(self, listener: ChannelListener, topic: str, timeout: int):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class RedisChannel(Channel):
    def __init__(self, host: str, port: int):
        self._client = Redis(host=host, port=port)
        self._stop = False

    def push(self, topic: str, message: Any):
        self._client.lpush(topic, json.dumps(message))

    def take(self, topic: str, timeout: int = 0) -> Any:
        data = self._client.brpop(topic, timeout)
        if data is None:
            return None
        response_data = json.loads(data[1].decode('utf-8'))
        return json.loads(response_data)

    def set(self, topic: str, message: Any):
        self._client.set(topic, message)

    def listen(self, listener: ChannelListener, topic: str, timeout: int = 0):
        while not self._stop:
            try:
                message = self.take(topic, timeout)
                listener.on_next(message)
            except Exception as e:
                listener.on_exception(e)
        listener.on_complete()

    def close(self):
        self._stop = True
        self._client.close()
