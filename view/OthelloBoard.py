import pygame

from model.Board import Board
from model.Item import Item
from model.SquareType import SquareType



class BoardView:
    def __init__(self):
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600
        self.boardScreen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.LINE_COLOR = (0, 0, 0)
        self.boardColor = (0, 250, 0)
        self.counter = 0

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

    def run(self):
        pygame.init()
        pygame.init()
        running = True
        myBoard = BoardView()
        screen = myBoard.boardScreen
        game = Board()
        speed = 1

        while running:

            screen.fill((255, 255, 255))
            myBoard.drawGrid()
            myBoard.drawBoard(game.board)
            myBoard.showValidMoves(game)
            if myBoard.counter == 100:
                speed = -1
            elif myBoard.counter == 0:
                speed = 1
            myBoard.counter += speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    myBoard.move(game, event)

            pygame.display.flip()


        pygame.quit()
        



myBoard = BoardView()
myBoard.run()
