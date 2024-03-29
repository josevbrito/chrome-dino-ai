# Imports
import pygame
import os
import random
import sys

pygame.init()

# GLOBAL CONSTANTS

# Screen
SCREEN_HEIGTH = 650
SCREEN_WIDTH = 1200
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
BG = [
    pygame.image.load(os.path.join('Assets/Other', 'Track.png'))
]
CLOUD = [
    pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
]

# Obstacles
SMALL_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
]
PTERODACTYL = [
    pygame.image.load(os.path.join("Assets/Pterodactyl", "Pterodactyl1.png")),
    pygame.image.load(os.path.join("Assets/Pterodactyl", "Pterodactyl2.png")),
]

# Font
FONT = pygame.font.Font('freesansbold.ttf', 20)


# CLASSES

# Dinosaur
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.jump_vel = self.JUMP_VEL
        self.step_index = 0

        self.image = RUNNING[0]
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())

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

# Cloud
class Cloud:
    def __init__(self):
        self.image = CLOUD[0]
        self.x = SCREEN_WIDTH + random.randint(800, 1000) 
        self.y = random.randint(50, 100)
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# Obstacle
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

# Small Cactus
class SmallCactus(Obstacle):
    def __init__(self, image, type):
        super().__init__(image, type)
        self.rect.y = 325

# Large Cactus
class LargeCactus(Obstacle):
    def __init__(self, image, type):
        super().__init__(image, type)
        self.rect.y = 300    

# Pterodactyl
class Pterodactyl(Obstacle):
    PTERODACTYL_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.PTERODACTYL_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def remove(index):
    dinosaurs.pop(index)



# Main
def main():
    # Initialization of necessary variables and objects to start the game
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs
    clock = pygame.time.Clock()
    points = 0
    cloud = Cloud()

    obstacles = []
    dinosaurs = [Dinosaur()]

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    # Function to update the game score and increase speed as needed
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points: {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (1050, 50))

    # Function to draw and scroll the game background 
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG[0].get_width()
        SCREEN.blit(BG[0], (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG[0], (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)
        
        # Check if there are no dinosaurs left
        if len(dinosaurs) == 0:
            break

        # Generate obstacles if there are none
        if len(obstacles) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand_int == 2:
                obstacles.append(Pterodactyl(PTERODACTYL))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    remove(i)

        # Get user input
        user_input = pygame.key.get_pressed()

        # Handle dinosaur actions based on user input
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

        # Draw and update the cloud, score, and background
        cloud.draw(SCREEN)
        cloud.update()
        score()
        background()
        clock.tick(30)
        pygame.display.update()


main()