from assets.services.brapi.api_handler import BrapiApiHandler
from assets.utils.validators.base_asset_validator import BaseAssertValidator


class BrapiApiAssetValidator(BaseAssertValidator):
    api_handler = BrapiApiHandler()

    def validate_asset(self) -> bool:
        if not self.data:
            return False
        return True
