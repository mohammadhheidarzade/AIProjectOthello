class Item:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

