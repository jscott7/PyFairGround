import pygame
class AddAmmoTarget(pygame.sprite.Sprite):
    """ A stationary target which, if hit, will add ammo"""
    def __init__(self, xpos, ypos):
        super(AddAmmoTarget, self).__init__()
        self.surf = pygame.Surface((20, 40))

        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
