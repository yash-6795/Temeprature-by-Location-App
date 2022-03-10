from abc import abstractmethod

from api_external_requests.external_api import ExternalAPI
from cache.cache_adaptor import CacheAdaptor


class DataManager:
    api_handler = ExternalAPI()
    cache_handler = CacheAdaptor.get_provider()

    @classmethod
    @abstractmethod
    def get_data(cls, *args, **kwargs):
        pass
