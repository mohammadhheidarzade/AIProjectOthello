from copy import copy, deepcopy

class AIPlayer:
    global cornerWeight = 15 # done
    global edgeWeight = 8   # done
    global flipCountWeight = 5
    global discCount = 1    # done
    global validMoves = 1   # done
    global lessValidEnemyMoves = 5
    global dangerZone = -2 # done
    def __init__(self, boardGame):
        self.turn = SquareType.BLACK
        self.boardGame = deepcopy(boardGame)
        self.board = self.boardGame.board

    def miniMax(self, boardGame, depth):
       
        validSquares = boardGame.squares

        if (depth == 0 or boardGame)

        for item in validSquares:
            copyBoardGame = deepcopy(boardGame)
            copyBoardGame.move(item.row, item.col)
            if item.SquareType.BLACK:
                self.miniMax(copyBoardGame)
            else:
                self.miniMax(copyBoardGame)

    def heuristic(self):
        score = 0
        for row in self.board:
            for item in row:
                if self.isDangerZone(item):
                    score += dangerZone
                elif self.isEdge(item):
                    score += edgeWeight
                else self.isCorner(item):
                    score += cornerWeight
                score += self.countValidMoves() * validMoves
                score += self.boardDiscCount * discCount
        return score

            
    def isDangerZone(self, item):
        return (1 <= item.row <= 6 and (item.col == 1 or item.col == 6)) or 
                (1 <= item.col <= 6 and (item.row == 1 or item.row == 6))

    def countValidMoves(self):
        counts = 0
         for row in self.board:
            for item in row:
                if self.isValid(item):
                    counts += 1
        return counts 

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
            elif self.board[i][j].val == SquareType.EMPTY:
                return False
        return False

    def isValidIJ(self, i, j):
        return 0 <= i <= 7 and 0 <= j <= 7
    
    def boardDiscCount(self):
        counts = 0
        for row in self.board:
            for item in row:
               if item.val == self.turn:
                   counts += 1
        return counts

    def isCorner(self, item):
        return  (item.row == 0 and item.col == 0) or
                (item.row == 0 and item.col == 7) or
                (item.row == 7 and item.col == 7) or
                (item.row == 7 and item.col == 0)

    def isEdge(self, item):
        return  item.row == 0 or item.row == 7 or item.col == 0 or item.col == 7


    def miniMaxAlphaBetaPruning(self):
        pass