import logging

from decouple import config

from assets.utils.handlers.asset_api_handler import AssetApiHandler

logger = logging.getLogger(__name__)


class BrapiApiHandler(AssetApiHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__base_api_url = config("BASE_BRAPI_API_URL")
        self.__api_key = config("BRAPI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Accept": "application/json",
        }

    def get_stock_data(self, symbol: str, endpoint: str = None) -> dict:
        endpoint = endpoint or "/quote/"
        url = f"{self.__base_api_url}{endpoint}{symbol}?modules=financialData"
        data = self.get(url=url, symbol=symbol)
        results = data.get("results", [])
        if not results:
            return None
        result = results[0]
        # TODO: The financialData is available just for Pro plan.
        return {"price": result.get("financialData", {}).get("currentPrice")}

    def get_crypto_data(self, symbol: str, endpoint: str = None) -> dict:
        endpoint = endpoint or "/v2/crypto"
        url = f"{self.__base_api_url}{endpoint}"
        self.url_params = {"coin": symbol}
        data = self.get(url=url, symbol=symbol)
        results = data.get("results", [])
        if not results:
            return None
        result = results[0]
        return {"price": result.get("financialData", {}).get("currentPrice")}

    def asset_price(self):
        if not self.data:
            raise ValueError(f"No price data found for {self.symbol} of type {self.asset_type}.")

        return self.data.get("price")
