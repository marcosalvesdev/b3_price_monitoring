from assets.services.brapi.asset_validator import BrapiApiAssetValidator


class AssetValidator:
    validator = BrapiApiAssetValidator

    def __init__(self, *args, **kwargs):
        self.validator_instance = self.validator(*args, **kwargs)
        self.is_valid = self.validator_instance.is_valid
