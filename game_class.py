from board_class import MinesweeperBoard

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

    def play_game(self):
        self.prompt_for_level()
        self.create_board()
        self.board.draw_board()
        finished = False
        while not finished:
            self.prompt_for_move()
            self.board.draw_board()
            finished = self.board.check_if_finished()
            if finished:
                print 'Hooray! You won!'

