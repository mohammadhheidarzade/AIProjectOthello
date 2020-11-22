from enum import Enum

class SquareType(Enum):
    EMPTY = 'n'
    WHITE = 'w'
    BLACK = 'b'
    VALID = 'v'

    def showFullName(self):
        if self.value == 'w':
            return 'WHITE'
        elif self.value == 'b':
            return 'BLACK'
        elif self.value == 'v':
            return 'VALID'
        else:
            return 'EMPTY'

    def __str__(self):
        return self.value
