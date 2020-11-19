from model.SquareType import SquareType
from model.Item import Item


class Board:

    def __init__(self):
        self.board = [[Item(row, col, SquareType.EMPTY) for col in range(0, 8)] for row in range(0, 8)]
        self.board[3][3].val = SquareType.WHITE
        self.board[3][4].val = SquareType.BLACK
        self.board[4][3].val = SquareType.BLACK
        self.board[4][4].val = SquareType.WHITE
        self.turn = SquareType.WHITE

    def printBoared(self):
        print('-------------------------------')
        for row in self.board:
            for item in row:
                print(item.val.value + ' | ', end='')
            print()

    def validSquares(self):
        squares = []
        for row in self.board:
            for item in row:
                if self.isValid(item):
                    squares.append(item)
        return squares

    def isValid(self, item):
        if item.val != SquareType.EMPTY:
            return False
        for diri in range(-1, 2):
            for dirj in range(-1, 2):
                if diri == dirj == 0:
                    continue
                if self.iterateBoaredForValidation(item.row, item.col, diri, dirj):
                    return True
        return False

    def iterateBoaredForValidation(self, i, j, diri, dirj):
        seenDiffTurnColor = False
        while self.isValidIJ(i + diri, j + dirj):
            i += diri
            j += dirj
            if self.board[i][j].val != self.turn and self.board[i][j].val != SquareType.EMPTY:
                seenDiffTurnColor = True
            if not seenDiffTurnColor:
                return False
            if seenDiffTurnColor and self.board[i][j].val == self.turn:
                return True
        return False

    def isValidIJ(self, i, j):
        return 0 <= i <= 7 and 0 <= j <= 7

if __name__ == '__main__':
    print(SquareType.BLACK)

    gameBoared = Board()
    for i in gameBoared.validSquares():
        print(f"col is {i.col + 1} and row is {i.row + 1}")
    print()
    # print(gameBoared.validSquares())
    print('==================================')
    gameBoared.printBoared()
