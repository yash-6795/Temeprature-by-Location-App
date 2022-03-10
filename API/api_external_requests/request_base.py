from abc import abstractmethod


class BaseExternalAPI:
    @classmethod
    @abstractmethod
    def get(cls, path):
        ...
