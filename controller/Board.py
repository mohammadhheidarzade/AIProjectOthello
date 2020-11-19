class Board:

    def __init__(self):
        self.board = [['n' * 8] * 8]
        self.board[3][3] = 'w'
        self.board[3][4] = 'b'
        self.board[4][3] = 'b'
        self.board[4][4] = 'w'
        self.turn = 'w'

    def validSquares(self, turn):
        squares = []
        for row, i in enumerate(self.board):
            for item, j in enumerate(row):
                self.isValid(turn, item, i, j)
                return squares

    def isValid(turn, item, i, j):
        for diri in range(-1, 2):
            for dirj in range(-1, 2):

    def isValidIJ(i, j):
        return 0 <= i <= 7 and 0 <= j <= 7
