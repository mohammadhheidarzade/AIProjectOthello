from model.Board import Board
from view.OthelloView import BoardView

class Othello:
    def __init__(self):
        self.boardGame = Board()
        self.myBoard = BoardView(self.boardGame)

    def playGame(self):
        self.myBoard.run()
