# Imports
import pygame
from config import *
import math
import random

class spriteSheet:
    # Utility class to load and parse sprite sheets
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_image(self, x, y, width, height):
        # Extracts image from sprite sheet
        image = pygame.Surface([width, height])
        image.set_colorkey(BLACK)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

class Player(pygame.sprite.Sprite):
    # Player sprite class
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.xchange = 0
        self.ychange = 0

        self.facing = 'down'
        self.animationloop = 1

        self.image = self.game.characterspriteSheet.get_image(3, 1, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.downanimations = [self.game.characterspriteSheet.get_image(3, 2, self.width, self.height),
                           self.game.characterspriteSheet.get_image(35, 2, self.width, self.height),
                           self.game.characterspriteSheet.get_image(68, 2, self.width, self.height)]

        self.upanimations = [self.game.characterspriteSheet.get_image(3, 34, self.width, self.height),
                         self.game.characterspriteSheet.get_image(35, 34, self.width, self.height),
                         self.game.characterspriteSheet.get_image(68, 34, self.width, self.height)]

        self.leftanimations = [self.game.characterspriteSheet.get_image(3, 98, self.width, self.height),
                           self.game.characterspriteSheet.get_image(35, 98, self.width, self.height),
                           self.game.characterspriteSheet.get_image(68, 98, self.width, self.height)]

        self.rightanimations = [self.game.characterspriteSheet.get_image(3, 66, self.width, self.height),
                            self.game.characterspriteSheet.get_image(35, 66, self.width, self.height),
                            self.game.characterspriteSheet.get_image(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_with_enemies()

        self.rect.x += self.xchange
        self.collide_with_blocks('x')
        self.rect.y += self.ychange
        self.collide_with_blocks('y')

        self.xchange = 0
        self.ychange = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.xchange -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.xchange += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.ychange -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.ychange += PLAYER_SPEED
            self.facing = 'down'

    def collide_with_blocks(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.xchange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.xchange < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.ychange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.ychange < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_with_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        
        if self.facing == 'down':
            if self.ychange == 0:
                self.image = self.game.characterspriteSheet.get_image(3, 2, self.width, self.height)
            else:
                self.image = self.downanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1
        
        if self.facing == 'up':
            if self.ychange == 0:
                self.image = self.game.characterspriteSheet.get_image(3, 34, self.width, self.height)
            else:
                self.image = self.upanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1
        
        if self.facing == 'left':
            if self.xchange == 0:
                self.image = self.game.characterspriteSheet.get_image(3, 98, self.width, self.height)
            else:
                self.image = self.leftanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1
        
        if self.facing == 'right':
            if self.xchange == 0:
                self.image = self.game.characterspriteSheet.get_image(3, 66, self.width, self.height)
            else:
                self.image = self.rightanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1

class Enemy(pygame.sprite.Sprite):
    # Enemy sprite class
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.xchange = 0
        self.ychange = 0

        self.facing = random.choice(['left', 'right'])
        self.animationloop = 1
        self.movementloop = 0
        self.maxtravel = random.randint(7, 30)

        self.image = self.game.enemyspriteSheet.get_image(3, 2, self.width, self.height)

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.leftanimations = [self.game.enemyspriteSheet.get_image(3, 98, self.width, self.height),
                           self.game.enemyspriteSheet.get_image(35, 98, self.width, self.height),
                           self.game.enemyspriteSheet.get_image(68, 98, self.width, self.height)]

        self.rightanimations = [self.game.enemyspriteSheet.get_image(3, 66, self.width, self.height),
                            self.game.enemyspriteSheet.get_image(35, 66, self.width, self.height),
                            self.game.enemyspriteSheet.get_image(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.xchange
        self.rect.y += self.ychange

        self.xchange = 0
        self.ychange = 0

    def movement(self):
        if self.facing == 'left':
            self.xchange -= ENEMY_SPEED
            self.movementloop -= 1
            if self.movementloop <= -self.maxtravel:
                self.facing = 'right'

        if self.facing == 'right':
            self.xchange += ENEMY_SPEED
            self.movementloop += 1
            if self.movementloop >= self.maxtravel:
                self.facing = 'left'

    def animate(self):
        
        if self.facing == 'left':
            if self.xchange == 0:
                self.image = self.game.enemyspriteSheet.get_image(3, 98, self.width, self.height)
            else:
                self.image = self.leftanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1
        
        if self.facing == 'right':
            if self.xchange == 0:
                self.image = self.game.enemyspriteSheet.get_image(3, 66, self.width, self.height)
            else:
                self.image = self.rightanimations[math.floor(self.animationloop)]
                self.animationloop += 0.1
                if self.animationloop >= 3:
                    self.animationloop = 1

class Block(pygame.sprite.Sprite):
    # Block sprite class
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrainspriteSheet.get_image(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    # Ground sprite class
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrainspriteSheet.get_image(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    # Button class for UI
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Comfortaa-Regular.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
class Attack(pygame.sprite.Sprite):
    # Attack sprite class for player attacks
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.animationloop = 0

        self.image = self.game.attackspriteSheet.get_image(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.rightanimation = [self.game.attackspriteSheet.get_image(0, 64, self.width, self.height),
                           self.game.attackspriteSheet.get_image(32, 64, self.width, self.height),
                           self.game.attackspriteSheet.get_image(64, 64, self.width, self.height),
                           self.game.attackspriteSheet.get_image(96, 64, self.width, self.height),
                           self.game.attackspriteSheet.get_image(128, 64, self.width, self.height)]

        self.downanimation = [self.game.attackspriteSheet.get_image(0, 32, self.width, self.height),
                           self.game.attackspriteSheet.get_image(32, 32, self.width, self.height),
                           self.game.attackspriteSheet.get_image(64, 32, self.width, self.height),
                           self.game.attackspriteSheet.get_image(96, 32, self.width, self.height),
                           self.game.attackspriteSheet.get_image(128, 32, self.width, self.height)]

        self.leftanimation = [self.game.attackspriteSheet.get_image(0, 96, self.width, self.height),
                           self.game.attackspriteSheet.get_image(32, 96, self.width, self.height),
                           self.game.attackspriteSheet.get_image(64, 96, self.width, self.height),
                           self.game.attackspriteSheet.get_image(96, 96, self.width, self.height),
                           self.game.attackspriteSheet.get_image(128, 96, self.width, self.height)]
        
        self.upanimation = [self.game.attackspriteSheet.get_image(0, 0, self.width, self.height),
                         self.game.attackspriteSheet.get_image(32, 0, self.width, self.height),
                         self.game.attackspriteSheet.get_image(64, 0, self.width, self.height),
                         self.game.attackspriteSheet.get_image(96, 0, self.width, self.height),
                         self.game.attackspriteSheet.get_image(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
    
    def animate(self):
        direction = self.game.player.facing
        
        if direction == 'up':
            self.image = self.upanimation[math.floor(self.animationloop)]
            self.animationloop += 0.5
            if self.animationloop >= 5:
                self.kill()

        if direction == 'down':
            self.image = self.downanimation[math.floor(self.animationloop)]
            self.animationloop += 0.5
            if self.animationloop >= 5:
                self.kill()
        
        if direction == 'left':
            self.image = self.leftanimation[math.floor(self.animationloop)]
            self.animationloop += 0.5
            if self.animationloop >= 5:
                self.kill()
        
        if direction == 'right':
            self.image = self.rightanimation[math.floor(self.animationloop)]
            self.animationloop += 0.5
            if self.animationloop >= 5:
                self.kill()