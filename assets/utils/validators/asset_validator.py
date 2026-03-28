from assets.utils.validators.base_asset_validator import BaseAssetValidator


class AssetValidator(BaseAssetValidator):
    def __init__(self, external_validator: BaseAssetValidator = None):
        if external_validator and not isinstance(external_validator, BaseAssetValidator):
            raise TypeError(
                "external_asset_validator must be an instance of BaseAssetValidator or None"
            )
        self.external_asset_validator = external_validator

    @property
    def is_valid(self) -> bool:
        return self.external_asset_validation()

    def external_asset_validation(self) -> bool:
        if not self.external_asset_validator:
            return True
        return self.external_asset_validator.is_valid
