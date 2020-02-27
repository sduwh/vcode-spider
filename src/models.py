from typing import Optional


class Base:
    def as_dict(self) -> dict:
        r = {}
        for k in dir(self):
            v = getattr(self, k)
            if not k.startswith("__") and not callable(v):
                r[k] = v
        return r


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


class Task(Base):
    def __init__(self, namespace: str, key: str):
        self.namespace: str = namespace
        self.key: str = key
