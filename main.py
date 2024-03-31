import enum
import pygame
import os
import random
import neat
import math
import sys
from tabnanny import check

import time

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

PTERODACTYL = [pygame.image.load(os.path.join("Assets/Pterodactyl", "Pterodactyl1.png")),
        pygame.image.load(os.path.join("Assets/Pterodactyl", "Pterodactyl2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

current_generation = 0

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    isAlive = True

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.points = 0
        self.jumpTimer = 0

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput == 0 and not self.dino_jump and time.time() - self.jumpTimer >= 0.83:
            self.jumpTimer = time.time()
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == 1 and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput == 1):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def is_alive(self):
        return self.isAlive

    def get_data(self, obstacles):
        if len(obstacles) == 0:
            return [100,100,100]
        return [obstacles[0].type, obstacles[0].rect.x, obstacles[0].rect.y]

    def get_reward(self, points):
        self.points = points
        return self.points * 0.1


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

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

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Pterodactyl(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 200
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def runSimulation(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score

    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    high_score = 0 

    nets = []
    dinosaurs = [] 
    
    def save_high_score(high_score):
        with open('high_score.txt', 'w') as file:
            file.write(str(high_score))

    def load_high_score():
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    high_score = load_high_score() 

    def score():
        global points, game_speed, high_score
        points += 1
        if points % 50 == 0:
            game_speed += 1

        if points > high_score:
            high_score = points
            save_high_score(high_score)

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

        text = alive_font.render("Died: " + str(died), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 530)
        SCREEN.blit(text, text_rect)

        text = alive_font.render("High Score: " + str(high_score), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 570) 
        SCREEN.blit(text, text_rect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        dinosaurs.append(Dinosaur())

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)

    global current_generation
    current_generation += 1

    timer = time.time()

    for dinosaur in dinosaurs:
        dinosaur.jumpTimer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        SCREEN.fill((255, 255, 255))
        # userInput = pygame.key.get_pressed()


        # player.draw(SCREEN)
        # player.update(userInput)
        still_alive = 0
        died = 0
        for i, dinosaur in enumerate(dinosaurs):
            if dinosaur.is_alive():
                still_alive += 1
                output = nets[i].activate(dinosaur.get_data(obstacles))
                choice = output.index(max(output))
                if choice == 0:
                    dinosaur.update(0)
                else:
                    dinosaur.update(1)
                genomes[i][1].fitness += dinosaur.get_reward(points)
            else:
                died += 1

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Pterodactyl(PTERODACTYL))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for dinosaur in dinosaurs:
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    dinosaur.isAlive = False
                    death_count += 1

        if still_alive == 0:
            break

        if time.time() - timer >= 17: 
            break

        for dinosaur in dinosaurs:
            if dinosaur.is_alive():
                dinosaur.draw(SCREEN)
        
         # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        SCREEN.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        SCREEN.blit(text, text_rect)

        text = alive_font.render("Died: " + str(died), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 530)
        SCREEN.blit(text, text_rect)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":

    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(runSimulation, 5000)

    