from abc import ABC
from typing import Optional


class Base:
    def keys(self):
        # select key for dict() method
        raise NotImplementedError

    def __getitem__(self, item):
        return getattr(self, item)


class Problem(Base):
    def __init__(self, namespace: str, key: str):
        self.origin: str = namespace
        self.origin_id: str = key
        self.title: Optional[str] = None
        self.time_limit: Optional[int] = None
        self.memory_limit: Optional[int] = None
        self.description: Optional[str] = None
        self.input: Optional[str] = None
        self.output: Optional[str] = None
        self.sample_input: Optional[str] = None
        self.sample_output: Optional[str] = None
        self.hint: Optional[str] = None
        self.source: Optional[str] = None
        self.language: Optional[list] = None

    def base_info(self):
        return self.origin + self.origin_id + self.title

    def keys(self):
        return ('origin',
                'origin_id',
                'title',
                'time_limit',
                'memory_limit',
                'description',
                'input',
                'output',
                'sample_input',
                'sample_output',
                'hint',
                'source',
                'language')


class Response(Base):
    FAIL = 0
    SUCCESS = 1
    ERROR = 2

    def __init__(self, code=1, data=None, message='success'):
        if data is None:
            data = {}
        self.code: Optional[int] = code
        self.data: Optional[dict] = data
        self.message: Optional[str] = message

    def keys(self):
        return ('code',
                'data',
                'message')


class Task(Base, ABC):
    def __init__(self, namespace: str, key: str, task_id=""):
        self.namespace: str = namespace
        self.key: str = key
        self.task_id = task_id

    def keys(self):
        return (
            'namespace',
            'key',
            'message'
        )


class TaskResult(Base, ABC):
    SUCCESS = 'success'
    FAIL = 'fail'

    def __init__(self, result=FAIL, task_id='', message=''):
        self.result = result
        self.task_id = task_id
        self.message = message

    def keys(self):
        return (
            'result',
            'task_id',
            'message'
        )
