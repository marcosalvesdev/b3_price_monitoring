from assets.utils.validators.base_asset_validator import BaseAssertValidator
from assets.services.hg.api_handler import HGApiHandler


class HgApiAssetValidator(BaseAssertValidator):

    def validate_asset(self) -> bool:
        if not self.data.get("results", {}).get(self.ticker):
            return False

        return True
