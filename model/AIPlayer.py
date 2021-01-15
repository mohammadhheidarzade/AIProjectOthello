from copy import copy, deepcopy
import math
from model.SquareType import SquareType
from model.Board import Board
from model.Item import Item

import time

import random



class MiniMaxValue:
    def __init__(self, score, item):
        self.score = score
        self.item = item

class AIPlayer:
    # cornerWeight = 120
    # edgeWeight = 20
    # flipCountWeight = 10
    # lessValidEnemyMoves = 2
    # dangerZone = -50

    discCount = 1
    validMoves = 1
    maxDepth = 4
    branch = 3
    squareScores = [[120, -20, 20,  5,  5, 20, -20, 120],
                    [-20, -40, -5, -5, -5, -5, -40, -20],
                    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                    [  5,  -5,  3,  3,  3,  3,  -5,   5],
                    [  5,  -5,  3,  3,  3,  3,  -5,   5],
                    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                    [-20, -40, -5, -5, -5, -5, -40, -20],
                    [120, -20, 20,  5,  5, 20, -20, 120]]
    

    machineLearningFitures = [120, 20, 5, 3, -5, -20, -40]
            # Values squaresScores, discCount, validMoves

    numberOfCalc = 0

    def __init__(self, boardGame, turn, playerFeatures = None):
        #self.turn = SquareType.BLACK
        self.turn = turn
        self.boardGame = deepcopy(boardGame)
        self.board = self.boardGame.board
        if playerFeatures != None:
            self.squareScores = playerFeatures

    def getNextMove(self):
        if (self.boardGame.isEnded):
            return
        start = time.time()
        item = self.miniMax(self.boardGame, 0, -math.inf, math.inf)
        end = time.time()   
        #print(end - start)     
        return (item.item.row, item.item.col)

    # also includes minimax with alpha beta pruning
    def miniMax(self, boardGame, depth, alpha, beta):
        self.numberOfCalc += 1

        if boardGame.isEnded:
            result = MiniMaxValue(500, None) # NONE
            return result

        if depth == self.maxDepth:
            tmpBoard = deepcopy(boardGame.board)
            self.board = boardGame.board
            score = self.heuristic()
            self.board = tmpBoard
            result = MiniMaxValue(score, None) # NONE
            return result

        validSquares = boardGame.squares
        if len(boardGame.squares) > self.branch:
            validSquares = self.heuristicForSquare(boardGame.squares, self.branch)
        
        itemTmp = None # NONE
        if boardGame.turn == self.turn:
            maxi = -math.inf
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

    
    def heuristicForSquare(self, validSquares, resNum):
        tempHeuristic = []
        for item in validSquares:
            tempHeuristic.append((self.squareScores[item.row][item.col], item))
        tempHeuristic.sort(key= lambda x: x[0])
        tempChance = []
        listLen = len(tempHeuristic)
        divisorNum = (listLen * (listLen - 1)) / 2
        if divisorNum == 0:
            return []
        
        tmpCh = 0
        for index in range(0, len(tempHeuristic)):
            tmpCh += (index + 1) / divisorNum 
            tempChance.append(tmpCh)
            
        cum_chance = tuple(tempChance)
        res = []
        resSize = 0
        while resSize < resNum:
            randomItem = random.choices(tempHeuristic, cum_weights = cum_chance, k = 1) 
            if randomItem[0][1] not in res:   
                res.append(randomItem[0][1])
                resSize += 1
        return res

    def heuristic(self):
        score = 0
        for row in self.board:
            for item in row:
                if item.val == SquareType.BLACK or item.val == SquareType.WHITE:
                    score += self.squareScores[item.row][item.col]
        score += self.countValidMoves() * self.validMoves
        score += self.boardDiscCount() * self.discCount
        return score

    def countValidMoves(self):
        return len(self.boardGame.squares)
    
    def boardDiscCount(self):
        if self.boardGame.turn == SquareType.WHITE:
            return self.boardGame.whiteCount
        elif self.boardGame.turn == SquareType.BLACK:
            return self.boardGame.blackCount