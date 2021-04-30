import pygame

# Import pygame.locals for easier access to constants
from pygame.locals import (
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    QUIT
)

pygame.init()

clock = pygame.time.Clock()

# Setup the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class PlayerGun(pygame.sprite.Sprite):
    """ The Gun Controled by the player."""
    def __init__(self):
        super(PlayerGun, self).__init__()
        self.surf = pygame.Surface((10, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ( SCREEN_WIDTH / 2, 4 * SCREEN_HEIGHT / 5 ))
        
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    """ Bullet fired by the gun."""
    def __init__(self, xpos, ypos):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        self.speed = -20

    # Move the bullet sprite and remove if it passes the top of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top < 0:
            self.kill()


# Instantiate PlayerGun
playerGun = PlayerGun()

# Create groups to hold sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(playerGun)

# The main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False    
       
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    # Only allow one bullet on screen at a time
    if pressed_keys[K_SPACE] and len(bullets) == 0:
        bullet = Bullet(playerGun.rect.left + (playerGun.rect.width / 2), playerGun.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)

    playerGun.update(pressed_keys)
    bullets.update()

    screen.fill((0,0,0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip the display
    pygame.display.flip()

    clock.tick(30)

pygame.quit()