from random import randint
import sys
import select

BRICK = "x"
SPACE = " "
NEWLINE = "\n"


def concatenate(generator):
    return ''.join(list(generator))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def reverse_rows(matrix):
    return [list(reversed(row)) for row in matrix]


def rotate_90_clockwise(matrix):
    # return [list(reversed(row)) for row in zip(*matrix)]
    return reverse_rows(transpose(matrix))


def rotate_90_counter_clockwise(matrix):
    return transpose(reverse_rows(matrix))


def paint_cell(cell):
    return BRICK if cell == 1 else SPACE


class TBlock(object):

    def __init__(self, height, width, top=None, left=None):
        self.matrix = [[1] * width] + [
            [0] * (width / 2) + [1] + [0] * (width - width / 2 - 1)
            ] * (height-1)
        self.top = top
        self.left = left
        self.height = height
        self.width = width

    def rotate_clockwise(self):
        self.matrix = rotate_90_clockwise(self.matrix)

    def rotate_counter_clockwise(self):
        self.matrix = rotate_90_counter_clockwise(self.matrix)


class Board(object):

    def __init__(self, height=35, width=30):
        self.height = height
        self.width = width
        self.matrix = [
            [1] + [0 for _ in range(width)] + [1]
            for __ in range(height)] + [[1 for _ in range(width + 2)]]

    def __str__(self):
        string = concatenate(paint_cell(cell) for cell in self.matrix[0])
        for row in self.matrix[1:-1]:
            string += NEWLINE
            string += concatenate(paint_cell(cell) for cell in row)
        string += NEWLINE
        string += concatenate(paint_cell(cell) for cell in self.matrix[-1])
        return string

    def can_fit(self, block, row, col):
        try:
            return all(c + self.matrix[row + ri][col + ci] in (0, 1)
                       for ri, r in enumerate(block.matrix)
                       for ci, c in enumerate(r))
        except IndexError:
            return False

    def place(self, block, y, x):
        for ri, r in enumerate(block.matrix):
            for ci, c in enumerate(r):
                self.matrix[y + ri][x + ci] += c
        block.top = y
        block.left = x

    def remove(self, block, y, x):
        for ri, r in enumerate(block.matrix):
            for ci, c in enumerate(r):
                self.matrix[y + ri][x + ci] -= c
        block.top = y
        block.left = x


def move_right(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top, block.left+1):
        board.place(block, block.top, block.left+1)
    else:
        board.place(block, block.top, block.left)


def move_left(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top, block.left-1):
        board.place(block, block.top, block.left-1)
    else:
        board.place(block, block.top, block.left)


def rotate_clockwise(board, block):
    board.remove(block, block.top, block.left)
    block.rotate_clockwise()
    if board.can_fit(block, block.top, block.left):
        board.place(block, block.top, block.left)
    else:
        block.rotate_counter_clockwise()
        board.place(block, block.top, block.left)


def rotate_counter_clockwise(board, block):
    board.remove(block, block.top, block.left)
    block.rotate_counter_clockwise()
    if board.can_fit(block, block.top, block.left):
        board.place(block, block.top, block.left)
    else:
        block.rotate_clockwise()
        board.place(block, block.top, block.left)


def move_down(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top+1, block.left):
        board.place(block, block.top+1, block.left)
    else:
        board.place(block, block.top, block.left)
        raise Exception


def place_on_top(board, block):
    top = 0
    left = randint(1, board.width-block.width)
    if board.can_fit(block, top, left):
        board.place(block, top, left)


def timed_input(n):
    rlist, _, __ = select.select([sys.stdin], [], [], n)
    if rlist:
        x = sys.stdin.readline().strip()
        return x
    else:
        return None

if __name__ == '__main__':
    h = raw_input("Enter board height [30]: ")
    w = raw_input("Enter board width [40]: ")
    prompt = """
        Enter
        a followed by Enter for moving left,
        d followed by Enter for moving right,
        w followed by Enter for clockwise,
        s followed by Enter for anticlockwise
        and just Enter for staying in same column.
        You will get 1 seconds to think. Press any key when you
        are ready to start
        """
    raw_input(prompt)
    if h == '':
        h = 30
    else:
        h = int(h)
    if w == '':
        w = 40
    else:
        w = int(w)
    board = Board(h, w)
    block = TBlock(height=randint(2, 4), width=randint(2, 4))
    place_on_top(board, block)
    print board
    x = timed_input(1)
    while x != 'EOF':
        try:
            move_down(board, block)
        except:
            block = TBlock(height=randint(2, 4), width=randint(2, 4))
            place_on_top(board, block)
        if x is not None:
            if x == 'a':
                move_left(board, block)
            elif x == 'd':
                move_right(board, block)
            elif x == 'w':
                rotate_clockwise(board, block)
            elif x == 's':
                rotate_counter_clockwise(board, block)
        print board
        x = timed_input(1)
