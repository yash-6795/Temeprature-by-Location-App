import os

from fastapi import FastAPI, HTTPException, Path
from data_manager.location_manager import LocationManager
from data_manager.temperature_manager import TemperatureManager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
location_manager = LocationManager
temperature_manager = TemperatureManager

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_geo_coord(location: str) -> tuple[str, str]:
    return location_manager.get_data(location)


@app.get("/temperature/{location}")
def get_temperature_data(location: str = Path(
    ...,
    min_length=1,
    regex="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$")
):
    location = location.replace(" ", "%20")
    try:
        resp = get_geo_coord(location)
        input_data = {
            'latitude': resp[1],
            'longitude': resp[0],
            'hourly': "temperature_2m"
        }
        resp = temperature_manager.get_data(location, **input_data)
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to serve the request at this moment, please try again "
                   "later!"
        )
