class ValueObject(object):
    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def __ne__(self, other: object) -> bool:
        return not self == other
