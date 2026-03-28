from unittest.mock import MagicMock

from django.test import TestCase

from assets.utils.validators.asset_validator import AssetValidator
from assets.utils.validators.base_asset_validator import BaseAssetValidator


class AssetValidatorTests(TestCase):
    def test_is_valid_true_when_no_external_validator(self):
        validator = AssetValidator()
        self.assertTrue(validator.is_valid)

    def test_is_valid_true_when_external_validator_passes(self):
        external = MagicMock(spec=BaseAssetValidator)
        type(external).is_valid = property(lambda self: True)
        validator = AssetValidator(external_validator=external)
        self.assertTrue(validator.is_valid)

    def test_is_valid_false_when_external_validator_fails(self):
        external = MagicMock(spec=BaseAssetValidator)
        type(external).is_valid = property(lambda self: False)
        validator = AssetValidator(external_validator=external)
        self.assertFalse(validator.is_valid)

    def test_init_raises_type_error_for_invalid_external_validator(self):
        with self.assertRaises(TypeError):
            AssetValidator(external_validator="not_a_validator")

    def test_is_valid_is_a_property(self):
        self.assertIsInstance(type(AssetValidator()).is_valid, property)
