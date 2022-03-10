from unittest import TestCase
from unittest.mock import patch

from data_manager.temperature_manager import TemperatureManager
from tests.test_location_manager import MockedResponseBase
from fastapi import HTTPException


class MockedResponseSuccess(MockedResponseBase):
    @classmethod
    def json(cls):
        return {
            "utc_offset_seconds": 0,
            "hourly_units": {"temperature_2m": "°C", "time": "iso8601"},
            "hourly": {
                "time": ["2022-03-10T00:00", "2022-03-10T01:00"],
                "temperature_2m": [8.9, 8.4]
            },
            "latitude": 51.52,
            "elevation": 24.5625,
            "longitude": -0.10000014,
            "generationtime_ms": 2.33304500579834
        }


class MockedResponseError(MockedResponseBase):
    status_code = 400

    @classmethod
    def json(cls):
        return {
            "error": True,
            "reason": "Error message"
        }


class TestTemperatureManagerTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.location = "London"
        cls.geo_data = ('-0.141589971037391', '51.51753')
        cls.input_data = {
            'latitude': '51.51753',
            'longitude': '-0.141589971037391',
            'hourly': "temperature_2m"
        }
        cls.temperature_manager = TemperatureManager
        cls.expected_data = [
            {'2022-03-10T00:00': 8.9}, {'2022-03-10T01:00': 8.4}
        ]

    @patch("data_manager.temperature_manager.TemperatureManager.check_cache")
    @patch("data_manager.data_manager_base.DataManager.api_handler")
    def test_get_data_from_api(self, mock_api_handler, mock_check_cache):
        mock_check_cache.return_value = False
        mock_api_handler.get.return_value = MockedResponseSuccess()
        ret = self.temperature_manager.get_data(self.location, **self.input_data)
        self.assertEqual(ret, self.expected_data)
        mock_check_cache.assert_called()
        mock_api_handler.get.assert_called()

    @patch("data_manager.data_manager_base.DataManager.cache_handler")
    @patch("data_manager.temperature_manager.TemperatureManager.check_cache")
    def test_get_data_from_cache(self, mock_check_cache, mock_cache_handler):
        mock_check_cache.return_value = True
        mock_cache_handler.get.return_value = [
            {'2022-03-10T00:00': 8.9}, {'2022-03-10T01:00': 8.4}
        ]
        ret = self.temperature_manager.get_data(self.location, **self.input_data)
        self.assertEqual(ret, self.expected_data)
        mock_check_cache.assert_called_with(self.location)
        mock_cache_handler.get.assert_called_with(self.location)

    @patch("data_manager.temperature_manager.TemperatureManager.check_cache")
    @patch("data_manager.data_manager_base.DataManager.api_handler")
    def test_get_data_api_exception(self, mock_api_handler,  mock_cache_check):
        mock_api_handler.get.return_value = MockedResponseError()
        mock_cache_check.return_value = False
        self.assertRaises(
            HTTPException,
            self.temperature_manager.get_data,
            self.location,
            **self.input_data
        )
        mock_cache_check.assert_called_with(self.location)



