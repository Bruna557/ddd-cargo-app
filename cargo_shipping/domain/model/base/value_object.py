"""Define the ValueObject base class."""


class ValueObject(object):
    """In DDD, a Value Object is an object that encapsulates a set of primitive
    values and related invariants.
    """

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def __ne__(self, other: object) -> bool:
        return not self == other

    def to_dict(self) -> dict:
        """Get a dictionary representation of the ValueObject."""

        raise NotImplementedError
