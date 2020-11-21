from enum import Enum

class SquareType(Enum):
    EMPTY = 'n'
    WHITE = 'w'
    BLACK = 'b'

    def showFullName(self):
        if self.value == 'w':
            return 'WHITE'
        elif self.value == 'b':
            return 'BLACK'
        else:
            return 'EMPTY'

    def __str__(self):
        return self.value
