from assets.services.brapi.api_handler import BrapiApiHandler
from assets.utils.validators.base_asset_validator import BaseAssertValidator


class BrapiApiAssetValidator(BaseAssertValidator):
    def __init__(self, ticker: str, asset_type: str, *args, **kwargs):
        self.ticker = ticker
        self.asset_type = asset_type
        self.api_handler = BrapiApiHandler(ticker=self.ticker, asset_type=self.asset_type)

    @property
    def is_valid(self) -> bool:
        data = self.api_handler.data
        return not (data and not data.get("results"))
