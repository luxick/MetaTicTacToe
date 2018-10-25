class Board:
    @staticmethod
    def make_board():
        return [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
        ]
    next_legal = ()

    def set(self, token, meta_board, field):
        self.next_legal = field
        x, y = meta_board
        m, n = field
        self.state[x][y][m][n] = token

    def __init__(self):
        self.state = self.make_board()
        for row in self.state:
            for i in range(len(row)):
                row[i] = self.make_board()

    def __getitem__(self, item):
        return self.state[item]

    def __len__(self):
        return len(self.state)

    def __str__(self):
        out = ''
        for x in range(3):
            out += ' ' + ' -------' * 3 + '\n'
            for z in range(3):
                out += ' | '
                for y in range(3):
                    out += ' '.join(self.state[x][y][z])
                    out += ' | '
                out += '\n'
        return out


if __name__ == '__main__':
    board = Board()
    board.set('X', (0, 0), (1, 2))
    board.set('O', (1, 2), (0, 0))
    board.set('X', (0, 0), (2, 1))
    board.set('O', (2, 1), (1, 1))

    print(board)