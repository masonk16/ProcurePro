from enum import Enum, IntEnum
from django.utils.translation import gettext_lazy as _


class UserType(IntEnum):
    CONTRACTOR = 1
    SUPPLIER = 2
    ADMIN = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
