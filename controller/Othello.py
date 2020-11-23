from model.Board import Board
from view.OthelloBoard import BoardView

boardGame = Board()
myBoard = BoardView(boardGame)
myBoard.run()
