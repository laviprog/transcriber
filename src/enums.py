from enum import Enum


class BaseEnum(str, Enum):
    """Base Enum"""

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns a list of all enum values.

        :return: A list of enum values.
        """

        return [item.value for item in cls]
