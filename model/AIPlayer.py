from copy import copy, deepcopy
import math
from model.SquareType import SquareType
from model.Board import Board
from model.Item import Item

import time



class MiniMaxValue:
    def __init__(self, score, item):
        self.score = score
        self.item = item

class AIPlayer:
    cornerWeight = 100 # done
    edgeWeight = 70   # done
    flipCountWeight = 10
    discCount = 1    # done
    validMoves = 1   # done
    lessValidEnemyMoves = 2
    dangerZone = -50 # done
    maxDepth = 5

    numberOfCalc = 0

    def __init__(self, boardGame):
        self.turn = SquareType.BLACK
        self.boardGame = deepcopy(boardGame)
        self.board = self.boardGame.board

    def getNextMove(self):
        if (self.boardGame.isEnded):
            return

        start = time.time()
        item = self.miniMax(self.boardGame, 0, -math.inf, math.inf)
        end = time.time()

        print(str(self.numberOfCalc) + ' ' + str(end - start) + ' ' + str((end - start) / self.numberOfCalc))
        return (item.item.row, item.item.col)

    # also includes minimax with alpha beta pruning
    def miniMax(self, boardGame, depth, alpha, beta):
       
        validSquares = boardGame.squares
        self.numberOfCalc += 1

        if boardGame.isEnded:
            result = MiniMaxValue(500, None)
            return result

        if depth == self.maxDepth:
            tmpBoard = deepcopy(boardGame.board)
            self.board = boardGame.board
            score = self.heuristic()
            self.board = tmpBoard
            result = MiniMaxValue(score, None)
            return result

        if boardGame.turn == SquareType.BLACK:
            maxi = -math.inf
            itemTmp = None
            validSquares = boardGame.squares
            for item in validSquares:
                copyBoardGame = deepcopy(boardGame)
                copyBoardGame.move(item.row, item.col)
                tmp = self.miniMax(copyBoardGame, depth + 1, alpha, beta)
                if maxi < tmp.score:
                    maxi = tmp.score
                    itemTmp = item
                if maxi >= beta:
                    return MiniMaxValue(maxi, itemTmp)
                alpha = max(alpha, maxi)
            return MiniMaxValue(maxi, itemTmp)
        else:
            mini = math.inf
            itemTmp = None
            validSquares = boardGame.squares
            for item in validSquares:
                copyBoardGame = deepcopy(boardGame)
                copyBoardGame.move(item.row, item.col)
                tmp = self.miniMax(copyBoardGame, depth + 1, alpha, beta)
                if mini > tmp.score:
                    mini = tmp.score
                    itemTmp = item
                if mini <= alpha:
                    return MiniMaxValue(mini, itemTmp)
                beta = min(beta, mini)
            return MiniMaxValue(mini, itemTmp)

    def heuristic(self):
        score = 0
        for row in self.board:
            for item in row:
                if item.val == SquareType.BLACK or item.val == SquareType.WHITE:
                    if self.isDangerZone(item):
                        score += self.dangerZone
                    elif self.isEdge(item):
                        score += self.edgeWeight
                    elif self.isCorner(item):
                        score += self.cornerWeight
        score += self.countValidMoves() * self.validMoves
        score += self.boardDiscCount() * self.discCount
        return score

    def isDangerZone(self, item):
        return (1 <= item.row <= 6 and (item.col == 1 or item.col == 6)) or (1 <= item.col <= 6 and (item.row == 1 or item.row == 6))

    def countValidMoves(self):
        return len(self.boardGame.squares)
    
    def boardDiscCount(self):
        if self.boardGame.turn == SquareType.WHITE:
            return self.boardGame.whiteCount
        elif self.boardGame.turn == SquareType.BLACK:
            return self.boardGame.blackCount

    def isCorner(self, item):
        return  (item.row == 0 and item.col == 0) or (item.row == 0 and item.col == 7) or \
                (item.row == 7 and item.col == 7) or \
                (item.row == 7 and item.col == 0)

    def isEdge(self, item):
        return  item.row == 0 or item.row == 7 or item.col == 0 or item.col == 7