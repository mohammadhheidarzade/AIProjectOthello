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
        self.squares = []
        self.validSquares()
        self.freezeCount = 0
        self.whiteCount = 2
        self.blackCount = 2
        self.isEnded = False

    def printBoared(self):
        print('-------------------------------')
        for row in self.board:
            for item in row:
                print(item.val.value + ' | ', end='')
            print()

    def validSquares(self):
        self.squares = []
        for row in self.board:
            for item in row:
                if self.isValid(item):
                    self.squares.append(item)

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

    def printOptions(self):
        print('-------------------------')
        for square in self.squares:
            print(f"row is {square.row + 1} and col is {square.col + 1}")

    def toggleTurn(self):
        if self.turn == SquareType.BLACK:
            self.turn = SquareType.WHITE
        else:
            self.turn = SquareType.BLACK

    def move(self, row, col):
        if len(self.squares) == 0:
            self.freezeCount += 1
            self.toggleTurn()
            return
        else:
            self.freezeCount = 0
        if self.freezeCount >= 2:
            print('Game finished')
            self.isEnded = True
            self.showFinalResult()
            return
        item = Item(row, col, SquareType.EMPTY)
        if not self.squares.__contains__(item):
            print('It\'s not a valid move')
            return
        for diri in range(-1, 2):
            for dirj in range(-1, 2):
                if self.iterateBoaredForValidation(row, col, diri, dirj):
                    self.changeColor(row, col, diri, dirj)

        self.toggleTurn()
        self.validSquares()

    def showFinalResult(self):
        print(f"White score is {self.whiteCount}")
        print(f"Black score is {self.blackCount}")
        if self.blackCount > self.whiteCount:
            print('Black player won!')
        elif self.blackCount < self.whiteCount:
            print('White player won')
        else:
            print('Tie!')
       # self.isEnded = True

    def changeColor(self, row, col, diri, dirj):
        self.board[row][col].val = self.turn
        self.updateScores(True)
        row += diri
        col += dirj
        while self.isValidIJ(row, col) and self.board[row][col].val != self.turn:
            self.board[row][col].val = self.turn
            self.updateScores(False)
            row += diri
            col += dirj

    def updateScores(self, isEmpty):
        if not isEmpty:
            if self.turn == SquareType.BLACK:
                self.blackCount += 1
                self.whiteCount -= 1
            else:
                self.whiteCount += 1
                self.blackCount -= 1
        else:
            if self.turn == SquareType.BLACK:
                self.blackCount += 1
            else:
                self.whiteCount += 1


if __name__ == '__main__':
    print(SquareType.BLACK)

    gameBoared = Board()
    for i in gameBoared.validSquares():
        print(f"col is {i.col + 1} and row is {i.row + 1}")
    print()
    # print(gameBoared.validSquares())
    print('==================================')
    gameBoared.printBoared()
