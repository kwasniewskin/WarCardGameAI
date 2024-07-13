import pygame
from game_logic import Game

# Initialize Pygame
pygame.init()

# Game window settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("War Card Game")

# Load assets
card_back = pygame.image.load("assets/ui_elements/card_back.png")
option_icon = pygame.image.load("assets/ui_elements/option_icon.png")
exit_icon = pygame.image.load("assets/ui_elements/exit_icon.png")

option_icon = pygame.transform.scale(option_icon, (50, 50))
exit_icon = pygame.transform.scale(exit_icon, (50, 50))
card_back = pygame.transform.scale(card_back, (112.5, 150))

# Colors
WHITE = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

# Initialize game
game = Game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle other events (clicks, keyboard, etc.)

    # Draw background
    screen.fill((150, 150, 150))

    # Draw UI elements
    round_text = font.render(f"Runda: {game.round}", True, WHITE)
    screen.blit(round_text, (10, 10))

    screen.blit(option_icon, (670, 10))
    screen.blit(exit_icon, (730, 10))

    # Opponent's deck
    screen.blit(card_back, (300, 30))

    # Played cards
    screen.blit(card_back, (200, 200))  # Opponent's played card
    screen.blit(card_back, (400, 200))  # My played card

    # My deck
    screen.blit(card_back, (300, 400))

    # Special cards
    joker_text = font.render("Joker", True, WHITE)
    x2_text = font.render("x2", True, WHITE)
    fifty_fifty_text = font.render("50/50", True, WHITE)

    screen.blit(joker_text, (500, 400))
    screen.blit(x2_text, (600, 400))
    screen.blit(fifty_fifty_text, (700, 400))

    # Refresh screen
    pygame.display.flip()

pygame.quit()
