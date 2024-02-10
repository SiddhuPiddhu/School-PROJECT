import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
ROCKET_WIDTH, ROCKET_HEIGHT = 50, 50
LASER_WIDTH, LASER_HEIGHT = 2, 10
BLOCK_WIDTH, BLOCK_HEIGHT = 50, 20
ROCKET_SPEED, LASER_SPEED, BLOCK_SPEED = 5, 10, 3
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE CLASHERS by Siddhant, Mayank, and Harsh")

# Set up the clock
clock = pygame.time.Clock()

# Define the Rocket class
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 0, 0), [(ROCKET_WIDTH//2, 0), (0, ROCKET_HEIGHT), (ROCKET_WIDTH, ROCKET_HEIGHT)])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - ROCKET_HEIGHT))
        self.speed = ROCKET_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, WIDTH - ROCKET_WIDTH))

# Define the Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = LASER_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Define the Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BLOCK_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    # Create the rocket
    rocket = Rocket()
    all_sprites.add(rocket)

    # Score
    score = 0

    # Game loop
    running = True
    while running:
        # Keep the loop running at the right speed
        clock.tick(60)

        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser = Laser(rocket.rect.centerx, rocket.rect.y)
                    lasers.add(laser)
                    all_sprites.add(laser)

        # Update
        all_sprites.update()

        # Check for collisions between lasers and blocks
        hits = pygame.sprite.groupcollide(blocks, lasers, True, True)
        for hit in hits:
            score += 1

        # Check for collisions between rocket and blocks
        if pygame.sprite.spritecollide(rocket, blocks, True):
            running = False

        # Add new blocks
        if len(blocks) < 5:
            block = Block(random.randint(0, WIDTH - BLOCK_WIDTH), 0)
            all_sprites.add(block)
            blocks.add(block)

        # Check if the blocks have reached the bottom
        if any(block.rect.top >= HEIGHT for block in blocks):
            running = False

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Flip the display
        pygame.display.flip()

    # Display final score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Final Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for a moment before quitting
    pygame.time.wait(2000)

def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main()
                if event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        text1 = font.render("Press '1' to Start", True, WHITE)
        text2 = font.render("Press '2' to Exit", True, WHITE)
        text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        pygame.display.flip()

if __name__ == "__main__":
    show_menu()
