from unittest.mock import patch

from fastapi.testclient import TestClient
from unittest import TestCase
from main import app
from parameterized import parameterized, parameterized_class


class TestAPIMain(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    @parameterized.expand([
        "London",
        "New York",
        "San Fran Cisco",
        "San-Francisco"
    ])
    @patch("main.get_geo_coord")
    def test_get_temperature_data_ok(self, location, mocked_method):
        # Mocking get_geo_coord ensures that out tests do not have dependency on co-ord api
        mocked_method.return_value = ("-.11", "51.52")
        response = self.client.get(f"/temperature/{location}")
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        " ",
        "     ",
        "   Dublin"
        "Dublin     "
        "Dublin-"
        "-Dublin"
    ])
    def test_get_temperature_data_exception(self, location):
        response = self.client.get(f"/temperature/{location}")
        self.assertEqual(response.json(), {'detail': 'Invalid input, please check the location provided!'})
        self.assertTrue(response.status_code != 200)

