import pygame
import random

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

class Counter():
    """ Keep track of score. """
    def __init__(self):
        self.SCORE = 0

    def UpdateScore(self):
        self.SCORE += 1

class PlayerGun(pygame.sprite.Sprite):
    """ The Gun Controlled by the player."""
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

class Target(pygame.sprite.Sprite):
    """ Target objects """
    def __init__(self, ypos, direction):
        super(Target, self).__init__()
        self.surf = pygame.Surface((20, 40))

        if random.randint(0, 1) == 0: 
            self.surf.fill((255, 255, 0))
        else:
            self.surf.fill((255, 0, 0))

        self.speed = 10
        self.direction = direction
        self.rect = self.surf.get_rect(center = (0, ypos))
        self.in_play = False

    def update(self):
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.in_play == False and self.rect.right > 60:
            self.in_play = True
        if self.rect.right > SCREEN_WIDTH:
            self.rect.move_ip(0, 50)
            self.direction = -self.direction
        if self.rect.left < 0:
            self.kill()
  
class Ammo(pygame.sprite.Sprite):
    """An available bullet displayed at the bottom of the screen"""
    def __init__(self, xpos):
        """
        Parameters
        ----------

        xpos : int
            The x screen position of the ammo sprite
        """
        super(Ammo, self).__init__()
        self.surf = pygame.Surface((10, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ( xpos, SCREEN_HEIGHT - 50 ))

    def UseAmmo(self):
        self.kill()

# Instantiate PlayerGun
playerGun = PlayerGun()

counter = Counter()
# Create font for score
font = pygame.font.SysFont(None, 48)
BLUE = pygame.Color(0, 0, 255)

max_targets = 20
ammo_count = 20

# Create groups to hold sprites
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()
ammunition = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(playerGun)

# Initialize the ammunition 
for i in range(1, ammo_count):
    cartridge = Ammo(20 * i)
    ammunition.add(cartridge)
    all_sprites.add(cartridge)

# TODO This is a bit buggy at the moment it doesn't update the ammo_count/sprite list correctly
def AddMoreAmmo(ammunition, all_sprites, ammo_count):
    remaining_ammo = len(ammunition)
    for i in range(1, 5):
        cartridge = Ammo(20 * (i + remaining_ammo))
        ammunition.add(cartridge)
        all_sprites.add(cartridge)
    
    return ammo_count + 5

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
        ammo_count -= 1
        if ammo_count > 0:
            ammunition.sprites()[-1].UseAmmo()
         
    if len(targets.sprites()) < max_targets:
        if all(x.in_play for x in targets.sprites()):
            new_target = Target(250, 1)
            targets.add(new_target)
            all_sprites.add(new_target)

    playerGun.update(pressed_keys)
    bullets.update()
    targets.update()

    # Check for bullet hitting target
    for bullet in bullets:
        targetsHit = pygame.sprite.spritecollide(bullet, targets, True)
        if len(targetsHit) > 0:
            bullet.kill()
            counter.UpdateScore()

    # Check for out of ammo
    if ammo_count == 1 and len(bullets) == 0:
        running = False

    # TODO : Add a target that can add more ammunition
    # if ammo_count == 2:
    #   ammo_count = AddMoreAmmo(ammunition, all_sprites, ammo_count)

    screen.fill((0,0,0))

    # Update the score
    img = font.render(str(counter.SCORE), True, BLUE)
   
    # blit is essentially copying the pixels from the sprite/image surface onto the screen surface
    screen.blit(img, (SCREEN_WIDTH - 100, 20))

    # Draw all the updated sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip the display
    # Updates the full display surface to the screen
    pygame.display.flip()

    clock.tick(30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
                running = False    

    img = font.render("GAME OVER!! HIT ANY KEY TO EXIT" , True, BLUE)
    screen.blit(img, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    pygame.display.flip()

pygame.quit()