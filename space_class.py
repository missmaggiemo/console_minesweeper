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
