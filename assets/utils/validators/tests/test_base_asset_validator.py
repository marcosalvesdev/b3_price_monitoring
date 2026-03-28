from django.test import TestCase

from assets.utils.validators.base_asset_validator import BaseAssetValidator


class BaseAssetValidatorTests(TestCase):
    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            BaseAssetValidator()

    def test_subclass_without_is_valid_cannot_be_instantiated(self):
        class Incomplete(BaseAssetValidator):
            pass

        with self.assertRaises(TypeError):
            Incomplete()

    def test_concrete_subclass_with_is_valid_can_be_instantiated(self):
        class Concrete(BaseAssetValidator):
            @property
            def is_valid(self) -> bool:
                return True

        instance = Concrete()
        self.assertTrue(instance.is_valid)
