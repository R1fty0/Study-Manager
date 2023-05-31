import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
BG_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Traffic Control")

# Aircraft variables
AIRCRAFT_RADIUS = 10
AIRCRAFT_SPEED = 2
aircraft_list = []

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Function to generate a new aircraft
def generate_aircraft():
    x = random.randint(AIRCRAFT_RADIUS, WIDTH - AIRCRAFT_RADIUS)
    y = 0
    dx = random.uniform(-1, 1) * AIRCRAFT_SPEED
    dy = random.uniform(0.5, 1.5) * AIRCRAFT_SPEED
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    aircraft = {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'color': color}
    aircraft_list.append(aircraft)

# Function to move the aircraft
def move_aircraft():
    for aircraft in aircraft_list:
        aircraft['x'] += aircraft['dx']
        aircraft['y'] += aircraft['dy']

# Function to remove aircraft that are off-screen
def remove_offscreen_aircraft():
    aircraft_list[:] = [aircraft for aircraft in aircraft_list if aircraft['y'] < HEIGHT]

# Function to check collision between aircraft
def check_collision():
    for i in range(len(aircraft_list)):
        for j in range(i + 1, len(aircraft_list)):
            dx = aircraft_list[i]['x'] - aircraft_list[j]['x']
            dy = aircraft_list[i]['y'] - aircraft_list[j]['y']
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= 2 * AIRCRAFT_RADIUS:
                return True

    return False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    # Generate new aircraft
    if len(aircraft_list) < 10:
        generate_aircraft()

    # Move and draw aircraft
    for aircraft in aircraft_list:
        pygame.draw.circle(screen, aircraft['color'], (int(aircraft['x']), int(aircraft['y'])), AIRCRAFT_RADIUS)

    # Update aircraft positions
    move_aircraft()
    remove_offscreen_aircraft()

    # Check collision
    if check_collision():
        score = 0
        aircraft_list.clear()

    # Draw score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    # Increase score
    score += len(aircraft_list) // 10

# Quit the game
pygame.quit()
