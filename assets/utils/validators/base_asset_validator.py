class BaseAssertValidator:
    @property
    def is_valid(self) -> bool:
        raise NotImplementedError("Subclasses must implement the is_valid property")
