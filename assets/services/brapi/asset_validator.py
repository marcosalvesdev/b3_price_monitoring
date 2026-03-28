from assets.services.brapi.api_handler import BrapiApiHandler
from assets.utils.validators.base_asset_validator import BaseAssetValidator


class BrapiApiAssetValidator(BaseAssetValidator):
    def __init__(self, symbol: str, asset_type: str, *args, **kwargs):
        self.symbol = symbol
        self.asset_type = asset_type
        self.api_handler = BrapiApiHandler(symbol=self.symbol, asset_type=self.asset_type)

    @property
    def is_valid(self) -> bool:
        data = self.api_handler.data
        return bool(data and data.get("results"))
