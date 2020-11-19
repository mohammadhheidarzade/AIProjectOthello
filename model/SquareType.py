from enum import Enum

class SquareType(Enum):
    EMPTY = 'n'
    WHITE = 'w'
    BLACK = 'b'

    def __str__(self):
        return self.value
