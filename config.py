# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from enum import Enum


class AddressMask(Enum):
    BIT_LENGTH: int = 0b000011000000000000000000
    STRAIGHT_ABSOLUTE: int = 0b0000
    INDIRECT_ABSOLUTE: int = 0b1010101
    WIDTH: int = 32
    ADDR_REFERENCE: int = 0b01011
