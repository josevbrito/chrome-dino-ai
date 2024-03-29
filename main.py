# Imports
import pygame
import os
import random
import sys

pygame.init()

# GLOBAL CONSTANTS

# Screen
SCREEN_HEIGTH = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

# Dinosaur Movement
RUNNING = [
    pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
    pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))
]

JUMPING = [
    pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))
]

DUCKING = [
    pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck1.png')),
    pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck2.png'))
]

# Landscape
TRACK = [
    pygame.image.load(os.path.join('Assets/Other', 'Track.png'))
]

CLOUD = [
    pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
]

# Dinosaur
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMPING[0]
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))



def main():
    clock = pygame.time.Clock()
    run = True
    font = pygame.font.Font('freesansbold.ttf', 20)
    dinosaurs = [Dinosaur()]




    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        user_input = pygame.key.get_pressed()

        for i, dinosaur in enumerate(dinosaurs):
            if (user_input[pygame.K_SPACE] or user_input[pygame.K_UP]) and not dinosaur.dino_jump:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False
                dinosaur.dino_duck = False
            elif user_input[pygame.K_DOWN] and not dinosaur.dino_jump:
                dinosaur.dino_duck = True
                dinosaur.dino_jump = False
                dinosaur.dino_run = False
            elif not (dinosaur.dino_jump or user_input[pygame.K_DOWN]):
                dinosaur.dino_duck = False
                dinosaur.dino_run = True
                dinosaur.dino_jump = False 

        clock.tick(30)
        pygame.display.update()

main()