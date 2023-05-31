import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 30
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create grid
grid = [[0] * COLS for _ in range(ROWS)]

# Generate maze
stack = [(0, 0)]
visited = set()
maze_generated = False

# Directions: Up, Right, Down, Left
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

while not maze_generated:
    if len(stack) == 0:
        maze_generated = True
        break

    x, y = stack[-1]
    visited.add((x, y))
    neighbors = []

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
            count = 0

            for j in range(4):
                ex = nx + dx[j]
                ey = ny + dy[j]

                if 0 <= ex < COLS and 0 <= ey < ROWS and (ex, ey) in visited:
                    count += 1

            if count == 1:
                neighbors.append((nx, ny))

    if len(neighbors) == 0:
        stack.pop()
    else:
        nx, ny = random.choice(neighbors)
        if nx > x:
            grid[y][x] |= 1  # Right
            grid[ny][nx] |= 4  # Left
        elif nx < x:
            grid[y][x] |= 4  # Left
            grid[ny][nx] |= 1  # Right
        elif ny > y:
            grid[y][x] |= 2  # Down
            grid[ny][nx] |= 8  # Up
        else:
            grid[y][x] |= 8  # Up
            grid[ny][nx] |= 2  # Down
        stack.append((nx, ny))

# Game loop
running = True
player_x = 0
player_y = 0

while running:
    clock.tick(FPS)

    # Process input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and (grid[player_y][player_x] & 4) == 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and (grid[player_y][player_x] & 1) == 0:
        player_x += 1
    if keys[pygame.K_UP] and (grid[player_y][player_x] & 8) == 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and (grid[player_y][player_x] & 2) == 0:
        player_y += 1

    # Render the maze
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] & 1:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE),
                                 (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
            if grid[y][x] & 2:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE),
                                 (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
            if grid[y][x] & 4:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE),
                                 (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
            if grid[y][x] & 8:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE),
                                 (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 2)

    # Draw the player
    pygame.draw.rect(screen, GREEN, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the exit
    pygame.draw.rect(screen, RED, ((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the screen
    pygame.display.flip()

pygame.quit()
