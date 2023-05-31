import pygame
import time

pygame.init()

# Set up the display
WIDTH = 300
HEIGHT = 200
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stopwatch")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

start_time = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_time is None:
                    start_time = time.time()
                else:
                    start_time = None

    screen.fill(BG_COLOR)

    if start_time is not None:
        elapsed_time = time.time() - start_time
        text = font.render(f"Time: {elapsed_time:.2f}", True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    else:
        text = font.render("Press SPACE to start", True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
