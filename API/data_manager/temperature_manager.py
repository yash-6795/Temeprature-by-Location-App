import datetime
from typing import Any

from fastapi import HTTPException
from data_manager.data_manager_base import DataManager


class TemperatureManager(DataManager):
    temp_data: dict = {}
    API_PATH = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def query_string_builder(delimiter: str, data: dict):
        return delimiter.join(
            f'{k}={v}' for k, v in data.items()
        )

    @staticmethod
    def parse_temp_data(data: dict) -> list[dict[Any, Any]]:
        time = data['hourly']['time']
        temp = data['hourly']['temperature_2m']
        output = [{_time: _temp} for _time, _temp in zip(time, temp)]
        return output

    @classmethod
    def get_data(cls, *args, **kwargs):
        location = args[0]
        if cls.check_cache(location):
            cached_data = cls.cache_handler.get(location)
            return cached_data

        query_string = cls.query_string_builder("&", kwargs)
        url = f"{cls.API_PATH}?{query_string}"

        resp = cls.api_handler.get(url)
        status_code, data = resp.status_code, resp.json()
        if status_code == 200 and "error" not in data:
            parsed_data = cls.parse_temp_data(data)
            cls.cache_handler.set(location, parsed_data)
            return parsed_data
        raise HTTPException(status_code=status_code, detail=data["reason"])

    @classmethod
    def check_cache(cls, key):
        cached_data = cls.cache_handler.get(key)
        if not cached_data:
            return False
        oldest_hour_forecast = list(cached_data[0].keys())[0]
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        if now > oldest_hour_forecast:
            # Invalidate cache
            return False
        return True
