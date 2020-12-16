import pygame

from model.Board import Board
from model.Item import Item
from model.ScreenType import ScreenType
from model.SquareType import SquareType
from model.AIPlayer import AIPlayer



class BoardView:
    def __init__(self, boardGame):
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600
        self.boardScreen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.LINE_COLOR = (0, 0, 0)
        self.boardColor = (0, 250, 0)
        self.endScreenColor = (0, 0, 0, 200)
        self.counter = 0
        self.running = False
        self.boardGame = boardGame

    def drawGrid(self):
        blockSize = 60  # Set the size of the grid block
        pygame.draw.rect(self.boardScreen, self.boardColor, pygame.Rect(60, 60, 480, 480), 0)
        for x in range(1, 9):
            for y in range(1, 9):
                rect = pygame.Rect(x * blockSize, y * blockSize,
                                   blockSize, blockSize)
                pygame.draw.rect(self.boardScreen, self.LINE_COLOR, rect, 1)

    def drawBoard(self, board):
        for row in board:
            for item in row:
                self.drawCircle(item, None)

    def drawCircle(self, item, turn):
        pos = ((item.row + 1) * 60 + 30, (item.col + 1) * 60 + 30)
        planetRadius = 20
        if item.val == SquareType.WHITE:
            planetColor = (255, 255, 255)
        elif item.val == SquareType.BLACK:
            planetColor = (0, 0, 0)
        elif item.val == SquareType.VALID:
            transparency = self.counter
            if turn == SquareType.WHITE:
                planetColor = (255, 255, 255, transparency + 30)
            else:
                planetColor = (0, 0, 0, transparency + 20)
            surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(surface, planetColor, pos, planetRadius)
            self.boardScreen.blit(surface, (0, 0))
            return
        else:
            return
        pygame.draw.circle(self.boardScreen, planetColor, pos, planetRadius)

    def move(self, board, event):
        if event.pos[1] % 60 == 0 or event.pos[0] % 60 == 0:
            return
        row = event.pos[0] // 60
        col = event.pos[1] // 60
        board.move(row - 1, col - 1)

    def showValidMoves(self, board):
        for square in board.squares:
            item = Item(square.row, square.col, SquareType.VALID)
            self.drawCircle(item, board.turn)

    def showScores(self, color):
        if color == 'b':
            score = self.boardGame.blackCount
            text = 'Black score : '
            pos = (440, 10)
        else:
            score = self.boardGame.whiteCount
            text = 'White score : '
            pos = (5, 10)
        largeFont = pygame.font.SysFont('comicsans', 30)
        scoreText = largeFont.render(text + str(score), 1, (0, 0, 0))
        self.boardScreen.blit(scoreText, pos)

    def showEndScreen(self):
        largeFont = pygame.font.SysFont('comicsans', 50)
        # main rect for end screen
        surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        rect = (40, 40, 520, 520)
        pygame.draw.rect(surface, self.endScreenColor, rect, 0)
        self.boardScreen.blit(surface, (0, 0))

        # button to restart
        # TODO
        surface2 = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        rect2 = (390, 420, 145, 55)
        pygame.draw.rect(surface2, (250, 0, 0, 150), rect2, 0)
        self.boardScreen.blit(surface2, (0, 0))
        buttonPos = (400, 430)
        endText = largeFont.render('Restart', 1, (255, 255, 255))
        self.boardScreen.blit(endText, buttonPos)

        # main text for end screen
        pos = (200, 100)
        endText = largeFont.render('Game Ended', 1, (250, 0, 0))
        self.boardScreen.blit(endText, pos)

        # score related texts
        winnerPos = (140, 250)
        if self.boardGame.whiteCount > self.boardGame.blackCount:
            winnerText = largeFont.render(f"White Player Won!!", 1, (255, 255, 255))
        elif self.boardGame.whiteCount < self.boardGame.blackCount:
            winnerText = largeFont.render(f"Black Player Won!!", 1, (255, 255, 255))
        else:
            winnerPos = (270, 250)
            winnerText = largeFont.render(f"Tie!!", 1, (255, 255, 255))
        self.boardScreen.blit(winnerText, winnerPos)

        pos2 = (100, 390)
        endScoreText = largeFont.render(f"White Score is {self.boardGame.whiteCount}", 1, (255, 255, 255))
        self.boardScreen.blit(endScoreText, pos2)

        pos3 = (100, 450)
        endScoreText2 = largeFont.render(f"Black Score is {self.boardGame.blackCount}", 1, (255, 255, 255))
        self.boardScreen.blit(endScoreText2, pos3)

    def restart(self, event):
        if 390 <= event.pos[0] <= 535 and 420 <= event.pos[1] <= 475:
            board = Board()
            self.boardGame = board

    def run(self):
        pygame.init()
        self.running = True
        speed = 1

        while self.running:
            self.boardScreen.fill((255, 255, 255))
            self.showScores('b')
            self.showScores('w')
            self.drawGrid()
            self.drawBoard(self.boardGame.board)
            self.showValidMoves(self.boardGame)
            if self.boardGame.isEnded:
                self.showEndScreen()
            if self.counter == 100:
                speed = -1
            elif self.counter == 0:
                speed = 1
            self.counter += speed

            if self.boardGame.turn == SquareType.BLACK:
                player = AIPlayer(self.boardGame)
                item = player.getNextMove()
                if not self.boardGame.isEnded:
                    self.boardGame.move(item[0], item[1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.boardGame.isEnded:
                    self.move(self.boardGame, event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.restart(event)


            pygame.display.flip()
        pygame.quit()
