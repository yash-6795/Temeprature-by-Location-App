import json

from pymemcache.client import base


class MemeCache:
    client = None

    def __init__(self, host, port):
        cls = self.__class__
        if not cls.client:
            cls.client = cls.conn(host, port)

    @classmethod
    def conn(cls, host, port):
        client = base.Client(f"{host}:{port}")
        return client

    def get(self, key):
        cls = self.__class__
        value = cls.client.get(key)
        if isinstance(value, str) or isinstance(value, bytes):
            value = json.loads(value)
        return value

    def set(self, key, value):
        cls = self.__class__
        if not isinstance(value, str):
            value = json.dumps(value)
        return cls.client.set(key, value)



