class TunelValidator:

    def __init__(self, lower_limit: [int, float], upper_limit: [int, float], interval: int):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.interval = interval

    @property
    def limits_are_valid(self) -> bool:
        return self.lower_limit < self.upper_limit

    @property
    def interval_is_valid(self) -> bool:
        return self.interval > 0
