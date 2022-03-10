from abc import abstractmethod
from unittest import TestCase
from unittest.mock import patch
from fastapi import HTTPException

from data_manager.location_manager import LocationManager


class MockedResponseBase:
    status_code = 200

    @classmethod
    @abstractmethod
    def json(cls):
        pass


class MockedResponseSuccess(MockedResponseBase):
    @classmethod
    def json(cls):
        return {
            "longt": "-0.141589971037391",
            "latt": "51.51753"
        }


class MockedResponseError(MockedResponseBase):
    status_code = 400

    @classmethod
    def json(cls):
        return {
            "error": {
                "description": "Error message",
                "code": "018"
            }
        }


class TestLocationManager(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.location_manager = LocationManager
        cls.location = "London"

    @patch("data_manager.data_manager_base.DataManager.cache_handler")
    @patch("data_manager.data_manager_base.DataManager.api_handler")
    def test_get_data_from_api(self, api_handler_mocked, cache_handler_mocked):
        dummy_response = MockedResponseSuccess()
        api_handler_mocked.get.return_value = dummy_response
        cache_handler_mocked.get.return_value = False
        ret = self.location_manager.get_data(self.location)
        self.assertEqual(ret, tuple(dummy_response.json().values()))

    @patch("data_manager.data_manager_base.DataManager.cache_handler")
    def test_get_data_from_cache(self, cache_handler_mocked):
        cache_handler_mocked.get.return_value = ('-0.141589971037391', '51.51753')
        ret = self.location_manager.get_data(self.location)
        self.assertEqual(ret, ('-0.141589971037391', '51.51753'))

    @patch("data_manager.data_manager_base.DataManager.cache_handler")
    @patch("data_manager.data_manager_base.DataManager.api_handler")
    def test_get_data_api_exception(self, api_handler_mocked, cache_handler_mocked):
        dummy_response = MockedResponseError()
        api_handler_mocked.get.return_value = dummy_response
        cache_handler_mocked.get.return_value = False
        self.assertRaises(
            HTTPException,
            self.location_manager.get_data,
            self.location
        )
