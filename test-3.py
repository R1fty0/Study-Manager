import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 400
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Board setup
board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

# Player setup
current_player = 'X'
winner = None

# Font setup
FONT_SIZE = 80
font = pygame.font.Font(None, FONT_SIZE)

# Calculate cell size
CELL_SIZE = WIDTH // 3

# Game loop
running = True

def draw_board():
    screen.fill(BG_COLOR)

    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), 3)
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, HEIGHT), 3)

    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), 3)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * 2), (WIDTH, CELL_SIZE * 2), 3)

    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            cell = board[row][col]
            if cell == 'X':
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, LINE_COLOR, (x - 25, y - 25), (x + 25, y + 25), 3)
                pygame.draw.line(screen, LINE_COLOR, (x - 25, y + 25), (x + 25, y - 25), 3)
            elif cell == 'O':
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, LINE_COLOR, (x, y), 25, 3)

def check_winner():
    global winner

    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            winner = board[row][0]
            return

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            winner = board[0][col]
            return

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        winner = board[0][0]
        return

    if board[0][2] == board[1][1] == board[2][0] != '':
        winner = board[0][2]
        return

    # Check for tie
    if all(cell != '' for row in board for cell in row):
        winner = 'tie'
        return

def restart_game():
    global board, current_player, winner
    board = [['', '', ''],
             ['', '', ''],
             ['', '', '']]
    current_player = 'X'
    winner = None

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
            # Get the coordinates of the clicked cell
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            # Update the board if the cell is empty
            if board[row][col] == '':
                board[row][col] = current_player
                check_winner()

                # Switch players
                if current_player == 'X':
                    current_player = 'O'
                else:
                    current_player = 'X'

    draw_board()

    # Draw the winner or tie message
    if winner:
        if winner == 'tie':
            message = "It's a tie!"
        else:
            message = f"Player {winner} wins!"

        text = font.render(message, True, LINE_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, BG_COLOR, text_rect)
        screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before restarting the game
        restart_game()

    pygame.display.flip()

# Quit the game
pygame.quit()
