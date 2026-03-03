from assets.utils.validators.base_asset_validator import BaseAssertValidator


class AssetValidator(BaseAssertValidator):
    def __init__(self, external_validator: BaseAssertValidator = None):
        if external_validator and not isinstance(external_validator, BaseAssertValidator):
            raise TypeError(
                "external_asset_validator must be an instance of BaseAssertValidator or None"
            )
        self.external_asset_validator = external_validator

    def is_valid(self) -> bool:
        return self.internal_asset_validation() and self.external_asset_validation()

    def internal_asset_validation(self):
        return True

    def external_asset_validation(self) -> bool:
        if not self.external_asset_validator:
            return True

        return self.external_asset_validator.is_valid
