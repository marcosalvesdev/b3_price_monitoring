from assets.utils.validators.base_asset_validator import BaseAssertValidator


class HgApiAssetValidator(BaseAssertValidator):
    def validate_asset(self) -> bool:
        if not self.data.get("results", {}).get(self.ticker):
            return False

        return True
