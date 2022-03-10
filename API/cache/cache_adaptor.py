import os

from cache.meme_cache import MemeCache


class CacheAdaptor:
    _host = os.environ.get("MEMECACHED_SERVICE_HOST", "localhost")
    _port = os.environ.get("MEMECACHED_SERVICE_PORT", "11211")

    @classmethod
    def get_provider(cls, provider_type="memecache"):
        if provider_type == "memecache":
            return MemeCache(cls._host, cls._port)

