import logging

import requests
from decouple import config

from global_utils.http_helpers import status_codes
from assets.utils.handlers.base_api_handler import BaseApiHandler

logger = logging.getLogger(__name__)


class BrapiApiHandler(BaseApiHandler):
    def __init__(self):
        super().__init__()
        self.__base_api_url = config("BASE_BRAPI_API_URL")
        self.__api_key = config("BRAPI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Accept": "application/json",
        }

    def get_stock_data(self, symbol: str, endpoint: str = None) -> dict:
        endpoint = endpoint or "/quote/"
        url = f"{self.__base_api_url}{endpoint}{symbol}"
        return self.get(url=url, symbol=symbol)

    def get_crypto_data(self, symbol: str, endpoint: str = None) -> dict:
        endpoint = endpoint or "/v2/crypto"
        url = f"{self.__base_api_url}{endpoint}"
        self.url_params = {"coin": symbol}
        return self.get(url=url, symbol=symbol)
