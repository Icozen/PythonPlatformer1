# # # Editor
# # Blocks
# Parameter1 = X-Coordinate
# Parameter2 = Y-Coordinate (The greater the subtraction, the higher the block; e.g. (height - blockSize*3) is one block higher than (height - blockSize*2))
# # # Features
# # New Features
# 1. Levels 1-3

import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Platformer")
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
FPS = 60
playerVelocity = 5

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def loadSpriteSheets(directory1, directory2, width, height, direction = False):
    path = join("assets", directory1, directory2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    allSprites = {

    }
    for image in images:
        spriteSheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(spriteSheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rectangle = pygame.Rect(i * width, 0, width, height)
            surface.blit(spriteSheet, (0, 0), rectangle)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            allSprites[image.replace(".png", "") + "_right"] = sprites
            allSprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            allSprites[image.replace(".png", "")] = sprites
    
    return allSprites

def getBlock(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # rect = pygame.Rect(96, 0, size, size)                   # Normal Block
    # rect = pygame.Rect(96, 64, size, size)                   # Autumn Block
    rect = pygame.Rect(96, 128, size, size)                   # Blossom Block
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# Classes
class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    gravity = 1
    SPRITES = loadSpriteSheets("MainCharacters", "MaskDude", 32, 32, True)
    animationDelay = 3
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.XMovement = 0
        self.YMovement = 0
        self.mask = None
        self.direction = "left"
        self.animationCount = 0
        self.fallCount = 0
        self.spriteSheet = "idle"
        self.hit = False
        self.hitCount = 0
    1.
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    2.
    def moveLeft(self, velocity):
        self.XMovement = -velocity
        if self.direction != "left":
            self.direction = "left"
            self.animationCount = 0
    3.
    def moveRight(self, velocity):
        self.XMovement = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animationCount = 0
    4.
    def landed(self):
        self.fallCount = 0
        self.YMovement = 0
        self.jumpCount = 0
    5.
    def hitHead(self):
        self.count = 0
        self.YMovement += 1
    6.
    def jump(self):
        self.YMovement = -self.gravity * 8
        self.animationCount = 0
        self.jumpCount += 1
        if self.jumpCount == 1:
            self.fallCount = 0
    7.
    def loop(self, fps):
        self.YMovement += min(1, (self.fallCount / fps) * self.gravity)
        self.move(self.XMovement, self.YMovement)
        if self.hit:
            self.hitCount += 1
        if self.hitCount > fps * 2:
            self.hit = False
            self.hitCount = 0
        self.fallCount += 1
        self.updateSprite()
    8.
    def updateSprite(self):
        if self.hit:
            self.spriteSheet = "hit"
        elif self.YMovement < 0:
            if self.jumpCount == 1:
                self.spriteSheet = "jump"
            elif self.jumpCount == 2:
                self.spriteSheet = "double_jump"
        elif self.YMovement > (self.gravity * 2):
            self.spriteSheet = "fall"
        elif self.XMovement != 0:
            self.spriteSheet = "run"
        elif self.XMovement == 0:
            self.spriteSheet = "idle"
        spriteSheetName = self.spriteSheet + "_" + self.direction
        sprites = self.SPRITES[spriteSheetName]
        spriteIndex = (self.animationCount // self.animationDelay) % len(sprites)
        self.sprite = sprites[spriteIndex]
        self.animationCount += 1
        self.update()
    9.
    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    10.
    def draw(self, window, offsetX):
        window.blit(self.sprite, ((self.rect.x - offsetX), self.rect.y))
    11.
    def makeHit(self):
        self.hit = True
        self.hitCount = 0
    

player = Player(100, 100, 50, 50)

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    1.
    def draw(self, screen, offsetX):
        screen.blit(self.image, ((self.rect.x - offsetX), self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = getBlock(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect = self.image.get_rect(center = (x + size // 2, y + size // 2))

class Fire(Object):
    animationDelay = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = loadSpriteSheets("Traps", "Fire", width, height)
        print(self.fire)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animationCount = 0
        self.animationName = "off"

    1.
    def on(self):
        self.animationName = "on"
    2.
    def off(self):
        self.animationName = "off"
    3.
    def loop(self):
        sprites = self.fire[self.animationName]
        spriteIndex = (self.animationCount // self.animationDelay) % len(sprites)
        self.image = sprites[spriteIndex]
        self.animationCount += 1
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if ((self.animationCount // self.animationDelay) > len(sprites)):
            self.animationCount = 0

class Level():
    def __init__(self):

        pass
    pass

class Level1(Level):
    def __init__(self):
        super().__init__()
        self.blocks = [Block()]
    pass

class Level2(Level):
    pass

class Level3(Level):
    pass
# Functions
1.
def getBackground(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, WIDTH, HEIGHT = image.get_rect()
    tiles = []
    for i in range(width // WIDTH + 1):
        for j in range(height // HEIGHT + 1):
            pos = (i * WIDTH, j * HEIGHT)
            tiles.append(pos)
    
    return tiles, image

2.
def handleVerticalCollision(player, objects, dy):
    collidedObjects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hitHead()
            
            collidedObjects.append(obj)
            
    return collidedObjects
3.
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collidedObject = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collidedObject = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collidedObject
4.
def handleMovement(player, objects):
    keys = pygame.key.get_pressed()
    player.XMovement = 0
    collideLeft = collide(player, objects, -playerVelocity * 2)
    collideRight = collide(player, objects, playerVelocity * 2)
    if keys[pygame.K_LEFT] and not collideLeft:
        player.moveLeft(playerVelocity) 
    if keys[pygame.K_RIGHT] and not collideRight:
        player.moveRight(playerVelocity)
    
    vericalCollide = handleVerticalCollision(player, objects, player.YMovement)
    toCheck = [collideLeft, collideRight, *vericalCollide]
    for obj in toCheck:
        if obj and obj.name == "fire":
            player.makeHit()
5.
def draw(window, background, bg_image, player, objects, offsetX):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offsetX)

    player.draw(window, offsetX)
    pygame.display.update()
6.
def main(screen):
    clock = pygame.time.Clock()
    background, bg_image = getBackground("Blue.png")
    # background, bgImage = getBackground("Purple.png")
    
    blockSize = 96
    player = Player(100, 100, 50, 50)
    fire = Fire(100, height - (blockSize * 1) - 64, 16, 32)
    fire.on()
    floor = [Block(i * blockSize, height - blockSize, blockSize) for i in range(-width // blockSize, 2 * width // blockSize)]
    objects = [
        *floor,
        Block(0, (height - blockSize * 2), blockSize),
        Block(blockSize * 3, (height - blockSize * 2), blockSize),
        Block(blockSize * 3, (height - blockSize * 3), blockSize),
        Block(blockSize * 6, (height - blockSize * 4), blockSize),
        Block(blockSize * 7, (height - blockSize * 4), blockSize),
        Block(blockSize * 8, (height - blockSize * 4), blockSize),
        Block(blockSize * 9, (height - blockSize * 4), blockSize),
        Block(blockSize * 13, (height - blockSize * 2), blockSize),
        Block(blockSize * 14, (height - blockSize * 2), blockSize),
        Block(blockSize * 14, (height - blockSize * 3), blockSize),
        Block(blockSize * 14, (height - blockSize * 4), blockSize),
        Block(blockSize * 14, (height - blockSize * 5), blockSize),
        Block(blockSize * 15, (height - blockSize * 5), blockSize),
        Block(blockSize * 16, (height - blockSize * 5), blockSize),
        Block(blockSize * 15, (height - blockSize * 3), blockSize),
        Block(blockSize * 18, (height - blockSize * 3), blockSize),
        Block(blockSize * 18, (height - blockSize * 4), blockSize),
        Block(blockSize * 18, (height - blockSize * 5), blockSize),
        Block(blockSize * 18, (height - blockSize * 6), blockSize),
        Block(blockSize * 18, (height - blockSize * 7), blockSize),
        Block(blockSize * 18, (height - blockSize * 8), blockSize),
        Block(blockSize * 18, (height - blockSize * 1), blockSize),
        Block(blockSize * 19, (height - blockSize * 3), blockSize),
        Block(blockSize * 20, (height - blockSize * 1), blockSize),
        Block(blockSize * 23, (height - blockSize * 5), blockSize),
        fire,
        ]

    offsetX = 0
    scrollAreaWidth = 100

    isGameRunning = True

    while isGameRunning:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameRunning = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jumpCount < 2:
                    player.jump()
        
        player.loop(FPS)
        fire.loop()
        handleMovement(player, objects)
        draw(screen, background, bg_image, player, objects, offsetX)
            
        if (((player.rect.right - offsetX) >= (width - scrollAreaWidth) and player.XMovement > 0) or ((player.rect.left + offsetX) <= (scrollAreaWidth) and player.XMovement < 0)):
            offsetX += player.XMovement
            pass

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(screen)