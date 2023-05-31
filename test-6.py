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
pygame.display.set_caption("Shooter Game")

# Player variables
player_size = 50
player_color = (255, 0, 0)
player_speed = 5
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_direction = None

# Bullet variables
bullet_size = 10
bullet_color = (0, 0, 255)
bullet_speed = 7
bullet_list = []

# Enemy variables
enemy_size = 50
enemy_color = (0, 255, 0)
enemy_speed = 2
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Game state variables
game_over = False
menu = True

# Shop variables
shop_open = False
shop_options = [
    {"name": "Turret", "price": 10, "description": "Place a turret that targets enemies"},
    {"name": "Barrier", "price": 5, "description": "Deploy a barrier that destroys 5 enemies before breaking"},
    {"name": "Bullets", "price": 3, "description": "Increase the number of bullets shot at once"}
]
selected_option = 0
player_coins = 0
turret_placed = False
barrier_deployed = False
extra_bullets = False


# Function to move the player
def move_player():
    if player_direction == "LEFT":
        player_pos[0] -= player_speed
    elif player_direction == "RIGHT":
        player_pos[0] += player_speed

    # Keep the player within the screen boundaries
    if player_pos[0] < 0:
        player_pos[0] = 0
    elif player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size


# Function to shoot a bullet
def shoot_bullet():
    if extra_bullets:
        bullet_pos1 = [player_pos[0], player_pos[1] - bullet_size]
        bullet_pos2 = [player_pos[0] + player_size - bullet_size, player_pos[1] - bullet_size]
        bullet_list.append(bullet_pos1)
        bullet_list.append(bullet_pos2)
    else:
        bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1] - bullet_size]
        bullet_list.append(bullet_pos)


# Function to move the bullets
def move_bullets():
    for bullet in bullet_list:
        bullet[1] -= bullet_speed


# Function to move the enemies
def move_enemies():
    for idx, enemy_pos in enumerate(enemy_list):
        enemy_pos[1] += enemy_speed


# Function to draw the player, bullets, enemies, and shop
def draw_objects():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    for bullet_pos in bullet_list:
        pygame.draw.rect(screen, bullet_color, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    coins_text = font.render("Coins: " + str(player_coins), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (WIDTH - coins_text.get_width() - 10, 10))

    if shop_open:
        draw_shop()

    pygame.display.flip()


# Function to display the game over screen
def game_over_screen():
    screen.fill(BG_COLOR)
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    restart_text = font.render("Press R to restart", True, (0, 0, 0))
    screen.blit(game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + score_text.get_height()))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height() * 2))
    pygame.display.flip()


# Function to display the main menu
def main_menu():
    screen.fill(BG_COLOR)
    title_text = font.render("Shooter Game", True, (0, 0, 0))
    start_text = font.render("Press S to start", True, (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + start_text.get_height()))
    pygame.display.flip()


# Function to display the shop
def draw_shop():
    shop_x = WIDTH // 2 - 150
    shop_y = HEIGHT // 2 - 150
    shop_width = 300
    shop_height = 300
    item_height = 50
    padding = 10

    pygame.draw.rect(screen, (200, 200, 200), (shop_x, shop_y, shop_width, shop_height))

    for idx, option in enumerate(shop_options):
        item_y = shop_y + idx * item_height + padding
        item_rect = pygame.Rect(shop_x + padding, item_y, shop_width - padding * 2, item_height - padding)

        if idx == selected_option:
            pygame.draw.rect(screen, (0, 0, 255), item_rect, 3)

        item_name = font.render(option["name"], True, (0, 0, 0))
        item_price = font.render("Price: " + str(option["price"]), True, (0, 0, 0))
        item_desc = font.render(option["description"], True, (0, 0, 0))

        screen.blit(item_name, (shop_x + padding * 2, item_y + padding))
        screen.blit(item_price, (shop_x + shop_width - item_price.get_width() - padding * 2, item_y + padding))
        screen.blit(item_desc, (shop_x + padding * 2, item_y + item_height // 2 - item_desc.get_height() // 2))


# Game loop
clock = pygame.time.Clock()
running = True

while running:
    while menu:
        main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False

    while game_over:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
                    bullet_list = []
                    enemy_list = [enemy_pos]
                    score = 0
                    player_coins = 0
                    turret_placed = False
                    barrier_deployed = False
                    extra_bullets = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                player_direction = "RIGHT"
            elif event.key == pygame.K_SPACE:
                shoot_bullet()
            elif event.key == pygame.K_q:
                shop_open = not shop_open

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_direction = None

    if not game_over:
        move_player()
        move_bullets()
        move_enemies()

        # Check for collisions between bullets and enemies
        for bullet_pos in bullet_list:
            if bullet_pos[1] < 0:
                bullet_list.remove(bullet_pos)
                continue

            for enemy_pos in enemy_list:
                if (
                        bullet_pos[0] >= enemy_pos[0]
                        and bullet_pos[0] < enemy_pos[0] + enemy_size
                        and bullet_pos[1] >= enemy_pos[1]
                        and bullet_pos[1] < enemy_pos[1] + enemy_size
                ):
                    enemy_list.remove(enemy_pos)
                    bullet_list.remove(bullet_pos)
                    score += 1
                    player_coins += 1

        # Check for collisions between player and enemies
        for enemy_pos in enemy_list:
            if (
                    enemy_pos[0] >= player_pos[0] - enemy_size
                    and enemy_pos[0] < player_pos[0] + player_size
                    and enemy_pos[1] >= player_pos[1] - enemy_size
                    and enemy_pos[1] < player_pos[1] + player_size
            ):
                game_over = True

        # Add new enemies at the top of the screen
        if len(enemy_list) < 5:
            if random.randint(0, 50) == 0:
                enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
                enemy_list.append(enemy_pos)

        draw_objects()
        clock.tick(60)

# Quit the game
pygame.quit()
