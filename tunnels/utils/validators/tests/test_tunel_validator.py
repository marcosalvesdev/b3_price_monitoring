from django.test import TestCase
from tunnels.utils.validators.tunnel_validator import TunelValidator


class TunelValidatorTestCase(TestCase):

    def test_limits_are_valid_when_lower_is_less_than_upper(self):
        validator = TunelValidator(lower_limit=1, upper_limit=10, interval=5)
        self.assertTrue(validator.limits_are_valid)

    def test_limits_are_invalid_when_lower_is_equal_to_upper(self):
        validator = TunelValidator(lower_limit=10, upper_limit=10, interval=5)
        self.assertFalse(validator.limits_are_valid)

    def test_limits_are_invalid_when_lower_is_greater_than_upper(self):
        validator = TunelValidator(lower_limit=15, upper_limit=10, interval=5)
        self.assertFalse(validator.limits_are_valid)

    def test_interval_is_valid_when_positive(self):
        validator = TunelValidator(lower_limit=1, upper_limit=10, interval=5)
        self.assertTrue(validator.interval_is_valid)

    def test_interval_is_invalid_when_zero(self):
        validator = TunelValidator(lower_limit=1, upper_limit=10, interval=0)
        self.assertFalse(validator.interval_is_valid)

    def test_interval_is_invalid_when_negative(self):
        validator = TunelValidator(lower_limit=1, upper_limit=10, interval=-5)
        self.assertFalse(validator.interval_is_valid)
