import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 50
BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Board setup
board = [['', 'b', '', 'b', '', 'b', '', 'b'],
         ['b', '', 'b', '', 'b', '', 'b', ''],
         ['', 'b', '', 'b', '', 'b', '', 'b'],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['r', '', 'r', '', 'r', '', 'r', ''],
         ['', 'r', '', 'r', '', 'r', '', 'r'],
         ['r', '', 'r', '', 'r', '', 'r', '']]

# Game variables
selected_piece = None
valid_moves = []

# Font setup
FONT_SIZE = 36
font = pygame.font.Font(None, FONT_SIZE)

# Function to draw the board
def draw_board():
    screen.fill(BG_COLOR)

    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = BLACK
            else:
                color = RED

            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            piece = board[row][col]
            if piece:
                piece_color = BLACK if piece == 'b' else RED
                pygame.draw.circle(screen, piece_color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    for move in valid_moves:
        pygame.draw.rect(screen, (0, 255, 0), (move[1] * CELL_SIZE, move[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def get_piece(row, col):
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return None
    return board[row][col]

def get_valid_moves(row, col):
    piece = board[row][col]
    moves = []

    if piece == 'b':
        moves.extend(get_valid_moves_for_piece(row, col, 1, 1))
        moves.extend(get_valid_moves_for_piece(row, col, 1, -1))
    elif piece == 'r':
        moves.extend(get_valid_moves_for_piece(row, col, -1, 1))
        moves.extend(get_valid_moves_for_piece(row, col, -1, -1))

    return moves

def get_valid_moves_for_piece(row, col, step_row, step_col):
    moves = []

    capture_row = row + step_row
    capture_col = col + step_col
    landing_row = row + step_row * 2
    landing_col = col + step_col * 2

    if get_piece(capture_row, capture_col) and not get_piece(landing_row, landing_col):
        moves.append((landing_row, landing_col))

    return moves

def select_piece(row, col):
    global selected_piece, valid_moves

    piece = board[row][col]
    if piece:
        selected_piece = (row, col)
        valid_moves = get_valid_moves(row, col)

def move_piece(row, col):
    global selected_piece, valid_moves

    if (row, col) in valid_moves:
        piece = board[selected_piece[0]][selected_piece[1]]
        board[selected_piece[0]][selected_piece[1]] = ''
        board[row][col] = piece

        selected_piece = None
        valid_moves = []

def restart_game():
    global board, selected_piece, valid_moves
    board = [['', 'b', '', 'b', '', 'b', '', 'b'],
             ['b', '', 'b', '', 'b', '', 'b', ''],
             ['', 'b', '', 'b', '', 'b', '', 'b'],
             ['', '', '', '', '', '', '', ''],
             ['', '', '', '', '', '', '', ''],
             ['r', '', 'r', '', 'r', '', 'r', ''],
             ['', 'r', '', 'r', '', 'r', '', 'r'],
             ['r', '', 'r', '', 'r', '', 'r', '']]

    selected_piece = None
    valid_moves = []

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            if selected_piece:
                move_piece(row, col)
            else:
                select_piece(row, col)

    draw_board()

    if selected_piece:
        pygame.draw.circle(screen, (0, 255, 0), (selected_piece[1] * CELL_SIZE + CELL_SIZE // 2, selected_piece[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    pygame.display.flip()

# Quit the game
pygame.quit()

