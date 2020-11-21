from model.Board import Board

if __name__ == "__main__":
    myGame = Board()

    while not myGame.isEnded:
        myGame.printBoared()
        myGame.printOptions()
        row, col = map(int, input(f"it\'s {myGame.turn.showFullName()} turn! Make your move").split(' '))
        myGame.move(row - 1, col - 1)