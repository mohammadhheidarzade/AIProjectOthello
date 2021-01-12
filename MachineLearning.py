import random
from copy import copy, deepcopy
from model.Board import Board
from enum import Enum
from model.SquareType import SquareType

from model.AIPlayer import AIPlayer


class GameFeatureState(Enum):
    Win = 'w'
    Equal = 'e'
    Lose = 'l'
class MachineLearningFeatures:

    def __init__(self):
        self.featureRange = 200
        self.numberOfFeatures = 7
        self.numberOfTeams = 2
        self.crossOverRate = 0.8
        self.mutationRate = 0.3
        self.geneticFeatures = []



    def randomBeginingPopulation(self):
        for i in range(0, self.numberOfTeams):
            temp = []
            for j in range(0, self.numberOfFeatures):
                temp.append(random.randint(-self.featureRange, self.featureRange))
            self.geneticFeatures.append(temp)


    # does cross over
    def doCrossOver(self, feature1, feature2):
        crossOverPoint1 = random.randint(0, self.numberOfFeatures - 1)
        crossOverPoint2 = random.randint(crossOverPoint1, self.numberOfFeatures - 1)

        while crossOverPoint2 - crossOverPoint1 == self.numberOfFeatures - 1:
            crossOverPoint2 = random.randint(crossOverPoint1, self.numberOfFeatures - 1)
        
        tempFeature1 = deepcopy(feature1)
        tempFeature2 = deepcopy(feature2)
        for i in range(crossOverPoint1, crossOverPoint2):
            tempFeature1[i] = (feature2[i])
            tempFeature2[i] = (feature1[i])
        
        return [tempFeature1, tempFeature2]

    # does mutation
    def doMutation(self, feature):
        randIndex = random.randint(0, self.numberOfFeatures - 1)
        randFeatureNum = random.randint(-self.featureRange, self.featureRange)
        feature[randIndex] = randFeatureNum
        return feature

    def doGeneticAlgorithm(self):
        allChilds = deepcopy(self.geneticFeatures)
        for ind1, feature1 in enumerate(self.geneticFeatures):
            for ind2, feature2 in enumerate(self.geneticFeatures):
                if ind1 <= ind2:
                    continue
                crossOverRandNum = random.uniform(0, 1)
                childs = []
                if crossOverRandNum <= self.crossOverRate:
                    childs = self.doCrossOver(feature1, feature2)
                    
                    for iChild in range(0, 2):
                        mutationRandNum = random.uniform(0, 1)
                        if mutationRandNum <= self.mutationRate:
                            childs[iChild] = self.doMutation(childs[iChild])
                            self.mutationRate *= 0.9

                    allChilds.append(childs[0])
                    allChilds.append(childs[1])
        self.geneticFeatures = allChilds


    def makeAIPlayerFeatures(self, feature):
        squareScores = [[120, -20, 20,  5,  5, 20, -20, 120],
                        [-20, -40, -5, -5, -5, -5, -40, -20],
                        [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                        [  5,  -5,  3,  3,  3,  3,  -5,   5],
                        [  5,  -5,  3,  3,  3,  3,  -5,   5],
                        [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                        [-20, -40, -5, -5, -5, -5, -40, -20],
                        [120, -20, 20,  5,  5, 20, -20, 120]]
        for ind1, row in enumerate(squareScores):
            for ind2, f in enumerate(row):
                if f == 120:
                    squareScores[ind1][ind2] = feature[0]
                if f == 20:
                    squareScores[ind1][ind2] = feature[1]
                if f == 5:
                    squareScores[ind1][ind2] = feature[2]
                if f == 3:
                    squareScores[ind1][ind2] = feature[3]
                if f == -5:
                    squareScores[ind1][ind2] = feature[4]
                if f == -20:
                    squareScores[ind1][ind2] = feature[5]
                if f == -40:
                    squareScores[ind1][ind2] = feature[6]

        return squareScores



    def doGame(self, feautre1, feautre2):
        boardGame = Board()


        while not boardGame.isEnded:
            player1 = AIPlayer(boardGame, SquareType.BLACK, self.makeAIPlayerFeatures(feautre1))
            item = player1.getNextMove()
            boardGame.move(item[0], item[1])

            player2 = AIPlayer(boardGame, SquareType.WHITE, self.makeAIPlayerFeatures(feautre2))
            item = player2.getNextMove()
            if not boardGame.isEnded:
                boardGame.move(item[0], item[1])

        result = []
        if boardGame.blackCount < boardGame.whiteCount:
            result.append(GameFeatureState.Lose)
            result.append(GameFeatureState.Win)
        elif  boardGame.blackCount > boardGame.whiteCount:
            result.append(GameFeatureState.Win)        
            result.append(GameFeatureState.Lose)
        else:
            result.append(GameFeatureState.Equal)
            result.append(GameFeatureState.Equal)
        return result


    def filterGeneticFeatures(self, scores):
        tempFeature = []
        for ind, score in enumerate(scores):
            tempFeature.append((score, ind))
        tempFeature.sort(key= lambda x: x[0])

        tempChance = []
        listLen = len(tempFeature)
        divisorNum = (listLen * (listLen - 1)) / 2
        if divisorNum == 0:
            return []
        
        tmpCh = 0
        for index in range(0, len(tempFeature)):
            tmpCh += (index + 1) / divisorNum 
            tempChance.append(tmpCh)
            
        cum_chance = tuple(tempChance)
        res = []
        resSize = 0
        while resSize < self.numberOfTeams:
            randomItem = random.choices(tempFeature, cum_weights = cum_chance, k = 1) 
            if randomItem[0][1] not in res:   
                res.append(randomItem[0][1])
                resSize += 1
        

        tmpGeneticFeatures = []
        for ind in res:
            tmpGeneticFeatures.append(self.geneticFeatures[ind])
        self.geneticFeatures = tmpGeneticFeatures

    def runGenetic(self):
        print(self.geneticFeatures)
        self.doGeneticAlgorithm()
        score = [0 for _ in range(0, len(self.geneticFeatures))]
        for ind1, feautre1 in enumerate(self.geneticFeatures):
            for ind2, feautre2 in enumerate(self.geneticFeatures):
                if ind1 == ind2:
                    continue
                res = self.doGame(feautre1, feautre2)
                if (res[0] == GameFeatureState.Equal):
                    score[ind1] += 1
                    score[ind2] += 1
                elif (res[0] == GameFeatureState.Win):
                    score[ind1] += 3
                elif (res[0] == GameFeatureState.Lose):
                    score[ind2] += 3
        self.filterGeneticFeatures(score)


ml = MachineLearningFeatures()
ml.randomBeginingPopulation()
for _ in range(0, 20):  
    ml.runGenetic()
