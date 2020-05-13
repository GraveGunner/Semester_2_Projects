# Final build of the Colour Sudoku game

import sys

import pygame

# Initializing colours
WHITE = (255, 255, 255)
b = BLACK = (0, 0, 0)
R = (255, 51, 51)
B = (51, 51, 255)
G = (51, 255, 51)
Y = (255, 255, 51)
colors = [b, R, G, B, Y]
GREY = (124, 124, 124)


class Board:
    boards = [[0, 3, 4, 0], [4, 0, 0, 2], [1, 0, 0, 3], [0, 2, 1, 0]]

    def __init__(self, rows, cols, width, height):
        """
        init the object
        :param rows: row
        :param cols: col
        :param width: width
        :param height: height
        """
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selection = False
        self.model = None
        self.boxes = [
            [Box(colors[self.boards[i][j]], i, j, width, height) for i in range(self.cols)] for j
            in
            range(self.rows)]

    def clear(self):
        """
        used to reset the temp_color to BLACK
        :return: None
        """
        row, col = self.selection
        if self.boxes[row][col].color == BLACK:
            self.boxes[row][col].set_temp_color(b)

    def draw(self, win):
        """
        used to draw the main window
        :param win: surface
        :return: None
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(win)

        gap = self.width / 4
        for i in range(self.rows + 1):
            if i % 2 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, GREY, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw_selection(win)

    def update_model(self):
        """
        used to updaate the model used to check success
        :return: None
        """
        self.model = [[colors.index(self.boxes[i][j].color)] for i in range(self.cols) for j in
                      range(self.rows)]

    def sketch(self, color):
        """
        used to set sketch the unsolved boxes
        :param color: color
        :return: None
        """
        row, col = self.selection
        self.boxes[row][col].set_temp_color(color)

    def select(self, row, col):
        """
        used to highlight a particular box
        :param row: row
        :param col: col
        :return: (row, col)
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selection = False

        self.boxes[row][col].selection = True
        self.selection = row, col

    def click(self, pos):
        """
        used to return the x amd y position of pointer
        :param pos: (x, y)
        :return: (int(y), int(x))
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 4
            x = pos[0] / gap
            y = pos[1] / gap
            return int(y), int(x)
        else:
            return None

    def finish_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].color == b:
                    return False
        return True

    def place(self, color):
        row, col = self.selection
        if self.boxes[row][col].color == b:
            self.boxes[row][col].set_color(color)
            self.update_model()

            if valid(self.model, colors.index(color), (row, col)) and solve(self.model):
                return True
            else:
                self.boxes[row][col].set_color(b)
                self.boxes[row][col].set_temp_color(b)
                self.update_model()
                return False


class Box:

    def __init__(self, color, row, col, width, height):
        """
        init the box
        :param color: color
        :param row: row
        :param col: col
        :param width: width
        :param height: height
        """
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selection = False
        self.color = color
        self.temp_color = b

    def draw(self, win):
        """
        used to draw the boxes
        :param win: surface
        :return: None
        """
        gap = self.width / 4
        x = self.col * gap
        y = self.row * gap
        box = pygame.Rect(x, y, gap, gap)
        if self.color == b and self.temp_color != b:
            pygame.draw.rect(win, self.temp_color, box)
        elif not self.color == b:
            pygame.draw.rect(win, self.color, box)

    def draw_selection(self, win):
        gap = self.width / 4
        x = self.col * gap
        y = self.row * gap
        box = pygame.Rect(x, y, gap, gap)
        if self.selection:
            pygame.draw.rect(win, WHITE, box, 5)

    def set_color(self, color):
        self.color = color

    def set_temp_color(self, color):
        self.temp_color = color


def redraw(win, board):
    """
    draw the window
    :param win: surface
    :param board: Board
    :return: None
    """
    win.fill(BLACK)
    board.draw(win)


def find_black(board):
    """
    used to find the unsolved boxes
    :param board: Board
    :return: (row, col)
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j

    return None


def valid(board, num, pos):
    """
    used to check if placement is valid or not
    :param board: Board
    :param color: int
    :param pos: (x, y)
    :return: Bool
    """
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 2
    box_y = pos[0] // 2

    for i in range(box_y * 2, box_y * 2 + 2):
        for j in range(box_x * 2, box_x * 2 + 2):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def solve(board):
    """
    used to solve the board using backtracking
    :param board: Board
    :return: Bool
    """
    find = find_black(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 5):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def main():
    win = pygame.display.set_mode((540, 540))
    img = pygame.image.load("Sud.png")
    pygame.display.set_icon(img)
    pygame.display.set_caption("COLOR SUDOKU")
    board = Board(4, 4, 540, 540)
    color = b
    wrongs = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = R
                if event.key == pygame.K_g:
                    color = G
                if event.key == pygame.K_b:
                    color = B
                if event.key == pygame.K_y:
                    color = Y
                if event.key == pygame.K_DELETE:
                    color = b
                    board.clear()
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    i, j = board.selection
                    if board.boxes[i][j].temp_color != b:
                        if board.place(board.boxes[i][j].temp_color):
                            print("Sucess")
                        else:
                            print("Wrong")
                            wrongs += 1
                            if wrongs >= 5:
                                print("Number of Guess Depleted\nGame Over")
                                run = False
                            else:
                                print("Number of Guesses Left ", 5 - wrongs)
                        color = b
                        if board.finish_board():
                            print("You Won\nGame Over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[1], clicked[0])
                    color = b

            if board.selection and color != b:
                board.sketch(color)

            redraw(win, board)
            pygame.display.update()

        redraw(win, board)


main()
sys.exit()
