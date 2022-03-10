from typing_extensions import Self
from api_external_requests.request_base import BaseExternalAPI
import requests


class ExternalAPI(BaseExternalAPI):
    @classmethod
    def get(cls, path):
        response = requests.get(path)
        return response
