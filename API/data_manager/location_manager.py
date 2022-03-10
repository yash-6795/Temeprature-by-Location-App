from .data_manager_base import DataManager
from fastapi import HTTPException


class LocationManager(DataManager):
    # locations should not be stored here since it will make the app stateful hence won't work when deployed as
    # distributed system Hence it is ideal to have data_adaptor that stores information in appropriate destination
    locations: dict = {}
    API_PATH = "https://geocode.xyz"

    @staticmethod
    def parse_coordinates(data):
        return (data['longt'], data['latt'])

    @classmethod
    def get_data(cls, *args, **kwargs) -> tuple[str, str]:
        location = args[0]
        url = f"{cls.API_PATH}/{location}?json=1"
        # Check in cache
        cached_resp = cls.cache_handler.get(f"geo_{location}")
        if cached_resp:
            return cached_resp

        resp = cls.api_handler.get(url)
        data, status_code = resp.json(), resp.status_code
        # If response OK, add data into cache to reduce external API calls
        # Vendor API seems to return 200 if there is an error
        # Consistent behaviour is data, response always has error property in dict
        # Hence decided to use error key to decide whether to return 200 or an Exception
        if "error" not in data:
            geo_cords = cls.parse_coordinates(data)
            cls.cache_handler.set(f"geo_{location}", geo_cords)
            return geo_cords
        raise HTTPException(
            status_code=status_code if status_code != 200 else 400,
            detail=cls.parse_error(data))

    @staticmethod
    def parse_error(data: dict):
        error_code = data['error']['code']
        if error_code in ["018", "007"]:
            return "Invalid location!"
        elif error_code == "006":
            return "Too many requests! Over Rate limit: up to 2 per sec."
        else:
            # Couldn't parse error message from response object
            # Return custom error response related to 4** error
            return "Bad Request!"
