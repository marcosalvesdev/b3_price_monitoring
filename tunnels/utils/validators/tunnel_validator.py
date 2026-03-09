class TunnelValidator:
    def __init__(
        self,
        lower_limit: int | float | None,
        upper_limit: int | float | None,
        interval: int | None,
    ):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.interval = interval

    @property
    def limits_are_valid(self) -> bool:
        if self.lower_limit is None or self.upper_limit is None:
            return False
        return self.lower_limit < self.upper_limit

    @property
    def interval_is_valid(self) -> bool:
        if self.interval is None:
            return False
        return self.interval > 0
