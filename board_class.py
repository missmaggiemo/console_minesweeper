import random

class MinesweeperSpace:
    def __init__(self):
        self.flag = self.cleared = self.has_mine = False

    def __str__(self):
        return "X" if self.has_mine else " "

    def __repr__(self):
        return "X" if self.has_mine else " "

    def toggle_flag(self):
        self.flag = not self.flag

    def set_cleared(self):
        if self.has_mine:
            raise ValueError("Oops! There's a mine here!")
        elif not self.cleared:
            self.cleared = True

    def set_mine(self):
        self.has_mine = True


class MinesweeperBoard:
    def __init__(self, height, width, mines):
        self.height, self.width, self.mines = (height, width, mines)
        self.grid = self.create_grid()

    def get_mine_places(self):
        mine_places = set()
        while len(mine_places) < self.mines:
            n = random.randint(0, self.height * self.width)
            # mine_places is list of tuples (row, col) where mines will be placed
            mine_places.add((int(n / self.width), int(n % self.height)))
        return mine_places

    def create_grid(self):
        grid = []
        for h in xrange(self.height):
            row = []
            for w in xrange(self.width):
                row.append(MinesweeperSpace())
            grid.append(row)
        mine_places = self.get_mine_places()
        for row, col in mine_places:
            grid[row][col].set_mine()
        return grid

    def draw_board(self):
        for line in self.grid:
            print line


board = MinesweeperBoard(10, 10, 2)
board.draw_board()
