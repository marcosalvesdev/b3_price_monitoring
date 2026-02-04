from decouple import config
import requests


class HGApiHandler:
    base_api_url = config("BASE_HG_API_URL")
    api_key = config("HG_API_KEY")

    def get_stock_data(self, symbol: str) -> dict:
        params = {
            "symbol": symbol.lower(),
            "key": self.api_key
        }
        response = requests.get(self.base_api_url, params=params)
        if response.status_code == 200:
            return response.json()
