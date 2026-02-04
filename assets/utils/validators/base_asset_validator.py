from assets.utils.handlers.base_api_handler import BaseApiHandler
from django.core.exceptions import ValidationError


class BaseAssertValidator:
    api_handler: BaseApiHandler = None

    def __init__(self, ticker: str, asset_type: str):
        if not isinstance(self.api_handler, BaseApiHandler):
            raise NotImplementedError("Subclasses must define an api_handler of type BaseApiHandler.")

        self.ticker = ticker
        self.asset_type = asset_type
        try:
            self.get_data = getattr(self.api_handler, f"get_{self.asset_type}_data")
        except AttributeError:
            raise ValidationError(
                f"Sorry, but our service does not support the {self.asset_type} asset type yet. "
                f"We are working on it!"
            )
        self.data = self.get_data(symbol=self.ticker)

    @property
    def is_valid(self) -> bool:
        return self.validate_asset()

    def validate_asset(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")
