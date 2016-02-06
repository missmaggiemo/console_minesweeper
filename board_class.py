import random, os
from space_class import MinesweeperSpace

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
            self.place_mine(grid, row, col)
        return grid

    def place_mine(self, grid, row, col):
        grid[row][col].set_mine()
        for i in [0, 1, -1]:
            for j in [0, 1, -1]:
                if row + i < 0 or col + j < 0:
                    continue
                try:
                    grid[row + i][col + j].add_value()
                except IndexError:
                    continue

    def get_valid_space(self, row, col):
        if row < 0 or col < 0:
            return
        try:
            space = self.grid[row][col]
        except IndexError:
            return
        return space

    def choose_space_to_clear(self, row, col):
        space = self.get_valid_space(row, col)
        if not space:
            raise ValueError

        if space.has_mine:
            print 'Game Over'
            raise ValueError
        else:
            self.clear_area(row, col, space.value)

    def clear_area(self, row, col, value):
        space = self.get_valid_space(row, col)
        if not space:
            return False
        elif space.cleared or space.value != value or space.has_mine:
            return False
        else:
            print (row, col, str(space))
            space.set_cleared()

        for i in [0, 1, -1]:
            for j in [0, 1, -1]:
                self.clear_area(row + i, col + j, value)

    def choose_space_to_flag(self, row, col):
        space = self.get_valid_space(row, col)
        if not space:
            raise ValueError
        else:
            space.toggle_flag()

    def check_if_finished(self):
        for i in xrange(len(self.grid)):
            for j in xrange(len(self.grid[0])):
                space = self.grid[i][j]
                if space.flag and not space.has_mine:
                    return False
                elif space.has_mine and not space.flag:
                    return False
        return True

    def draw_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, line in enumerate(self.grid):
            print '{} {} {}'.format(str(i).zfill(2), line, str(i).zfill(2))
