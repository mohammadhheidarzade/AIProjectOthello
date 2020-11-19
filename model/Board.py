from model.Item import Item


class Board:

    def __init__(self):
        self.board = [[Item(row, col, 'n') for col in range(0, 8)] for row in range(0, 8)]
        self.board[3][3].val = 'w'
        self.board[3][4].val = 'b'
        self.board[4][3].val = 'b'
        self.board[4][4].val = 'w'
        self.turn = 'b'

    def printBoared(self):
        print('-------------------------------')
        for row in self.board:
            for item in row:
                print(item.val + ' | ', end='')
            print()

    def validSquares(self):
        squares = []
        for row in self.board:
            for item in row:
                if self.isValid(item):
                    squares.append(item)
        return squares

    def isValid(self, item):
        if item.val != 'n':
            return False
        for diri in range(-1, 2):
            for dirj in range(-1, 2):
                if diri == dirj == 0:
                    continue
                if self.iterateBoaredForValidation(item.row, item.col, diri, dirj):
                    return True
        return False

    def iterateBoaredForValidation(self, i, j, diri, dirj):
        tmp1 = i
        tmp2 = j
        seenDiffTurnColor = False
        while self.isValidIJ(i + diri, j + dirj):
            i += diri
            j += dirj
            if self.board[i][j].val != self.turn and self.board[i][j].val != 'n':
                # print(f"{i + 1} {j + 1} boared is {self.board[i][j].val}")
                seenDiffTurnColor = True
            if not seenDiffTurnColor:
                return False
            if seenDiffTurnColor and self.board[i][j].val == self.turn:
                # print(f"boared is {self.board[tmp1][tmp2].val} before {tmp1 + 1} {tmp2 + 1} and after {i + 1} {j + 1}")
                return True
        return False

    def isValidIJ(self, i, j):
        return 0 <= i <= 7 and 0 <= j <= 7


# print(__name__)

if __name__ == '__main__':
    gameBoared = Board()
    for i in gameBoared.validSquares():
        print(f"col is {i.col + 1} and row is {i.row + 1}")
    print()
    # print(gameBoared.validSquares())
    print('==================================')
    gameBoared.printBoared()
