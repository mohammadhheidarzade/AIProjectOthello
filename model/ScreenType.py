from enum import Enum

class ScreenType(Enum):
    END = 'e'
    MAIN = 'm'


    def __str__(self):
        return self.value
