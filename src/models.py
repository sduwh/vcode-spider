from typing import Optional


class Base:
    def keys(self):
        # select key for dict() method
        raise NotImplementedError

    def __getitem__(self, item):
        return getattr(self, item)


class Problem(Base):
    def __init__(self, namespace: str, key: str):
        self.namespace: str = namespace
        self.key: str = key
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

    def keys(self):
        return ('namespace',
                'key',
                'title',
                'time_limit',
                'memory_limit',
                'description',
                'input',
                'output',
                'sample_input',
                'sample_output',
                'hint',
                'source')


class Task(Base):
    def __init__(self, namespace: str, key: str):
        self.namespace: str = namespace
        self.key: str = key
