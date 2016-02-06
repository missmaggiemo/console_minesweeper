import random, os, sys

class MinesweeperSpace:
    def __init__(self):
        self.flag = self.cleared = self.has_mine = False
        self.value = 0

    def __str__(self):
        return '<MinesweeperSpace flag={}, cleared={}, has_mine={}, value={}>'.format(
            self.flag, self.cleared, self.has_mine, self.value)

    def __repr__(self):
        if self.flag:
            return 'F'
        elif self.cleared:
            return str(self.has_mine or self.value or ' ')
        else:
            return 'X'

    def toggle_flag(self):
        self.flag = not self.flag

    def set_cleared(self):
        if self.has_mine:
            raise ValueError("Oops! There's a mine here!")
        elif not self.cleared:
            self.cleared = True

    def set_mine(self):
        self.has_mine = 'M'

    def add_value(self):
        self.value += 1


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


class MinesweeperGame:
    LEVEL_SETTINGS = {'Hard': (40, 40, 100), 'Medium': (30, 30, 30), 'Easy': (20, 20, 5)}

    def __init__(self):
        self.board = self.level = None

    def get_user_response(self, question, acceptable_answers):
        acceptable_answer = None
        while not acceptable_answer:
            raw_answer = raw_input(question)
            if raw_answer in acceptable_answers:
                acceptable_answer = raw_answer
        return acceptable_answer

    def prompt_for_level(self):
        level_response_options = {'H': 'Hard', 'Hard': 'Hard', 'Medium': 'Medium',
                                  'M': 'Medium', 'E': 'Easy', 'Easy': 'Easy'}
        question = 'What level would you like to play at-- Easy (E), Medium (M), or Hard (H)?  '
        level = self.get_user_response(question, level_response_options.keys())
        self.level = level_response_options.get(level)

    def prompt_for_action(self):
        action_options = {'F': 'Flag', 'Flag': 'Flag', 'C': 'Clear', 'Clear': 'Clear'}
        question = 'What woud you like to do?  Flag (F) or Clear (C)?  '
        action = self.get_user_response(question, action_options.keys())
        return action_options.get(action)

    def prompt_for_space_choice(self):
        question = 'What space would you like to explore-- row(int), col(int)?  '
        raw_output = raw_input(question)
        try:
            row, col = [int(d) for d in raw_output.split(', ')]
            self.board.grid[row][col]
        except Exception as e:
            print e
            self.prompt_for_space_choice()
        return (row, col)

    def prompt_for_move(self):
        row, col = self.prompt_for_space_choice()
        action = self.prompt_for_action()
        if action == 'Flag':
            self.board.choose_space_to_flag(row, col)
        elif action == 'Clear':
            self.board.choose_space_to_clear(row, col)

    def check_if_finished(self):
        if game.board.check_if_finished():
            return True
        return False

    def create_board(self):
        self.board = MinesweeperBoard(*self.LEVEL_SETTINGS.get(self.level))


game = MinesweeperGame()
game.prompt_for_level()
game.create_board()
game.board.draw_board()
finished = False
while not finished:
    game.prompt_for_move()
    game.board.draw_board()
    finished = game.board.check_if_finished()
    if finished:
        print 'Hooray! You won!'
