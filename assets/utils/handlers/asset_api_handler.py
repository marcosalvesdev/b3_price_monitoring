from django.core.exceptions import ValidationError

from assets.utils.handlers.base_api_handler import BaseApiHandler


class AssetApiHandler(BaseApiHandler):
    def __init__(self, ticker: str = None, asset_type: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker
        self.asset_type = asset_type

    @property
    def data(self):
        try:
            get_asset_data = getattr(self, f"get_{self.asset_type}_data")
            return get_asset_data(symbol=self.ticker)
        except AttributeError:
            raise ValidationError(
                f"Sorry, but our service does not support the {self.asset_type} asset type yet. "
                f"We are working on it!"
            ) from None

    def get_asset_price(self):
        raise NotImplementedError("This method should be implemented in the subclass.")
