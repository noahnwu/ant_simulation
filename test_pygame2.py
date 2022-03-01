# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 11:15:35 2022

@author: noahf
"""

import pygame
from random import randint
from math import copysign
GRAY = (100, 100, 100 )
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)


class Ant(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        self.size = size
        pygame.sprite.Sprite.__init__(self)
        self.carry = 0
        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.steps = 0
        self.speed = 1
        self.pher_delay = 0
        self.forage = True
    def change_dx(self): 
        self.dx = self.dx * -1
        self.dy = self.dy * -1 
        
    def update(self): 
        
        if self.steps == 0:
            self.dx = randint(-1, 1)
            self.dy = randint(-1, 1)
        self.steps += 1
        if self.forage == True: 
            if self.steps == 20: 
                self.steps = randint(0, 10)
        
        elif self.forage == False: 
            if self.steps == 20:
                self.steps = randint(0, 10)
            
        if self.rect.center[0] <= 0 or self.rect.center[0] >= bounds: 
            self.dx = self.dx *-1
        if self.rect.center[1] <= 0 or self.rect.center[1] >= bounds: 
            self.dy = self.dy * -1
        
        self.rect.center = (self.rect.center[0] + (self.dx*self.speed), 
                            self.rect.center[1] + (self.dy*self.speed))
            
    
    def collide(self): 
            self.carry = 1
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(GREEN)
            self.rect.size = (self.size, self.size) 
            self.change_dx()
            self.forage = False
            
    def dropoff(self): 
        self.carry = 0
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(GRAY)
        self.rect.size = (self.size, self.size) 
        self.change_dx()
        self.forage = True

    def pher_prod(self): 
        self.pher_delay += 1 
        if self.pher_delay >= 20: 
            self.pher_delay = 0
    def food_locate(self, food_source): 
        self.food_location = food_source
            
        
            
        
class Food(pygame.sprite.Sprite):
    def __init__(self, size):
        self.size = size
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def cursor_move(self): 
        self.pos = pygame.mouse.get_pos()
        self.rect.center = self.pos
        self.draw(screen)
    def hold(self): 
        self.pos = pygame.mouse.get_pos()
        self.rect.center = self.pos
    def shrink(self): 
        self.size = self.size * 0.9
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(GREEN)
        self.rect.size = (self.size, self.size)
        if self.size < 10: 
            self.kill()
        
        
class Nest(pygame.sprite.Sprite): 
    def __init__(self):
        size = 100
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (bounds/2, bounds/2)
    def draw(self): 
        screen.blit(self.image, self.rect)

class Pheromone(pygame.sprite.Sprite): 
    def __init__(self, size, pos, target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.alpha = 255
        self.blit_switch = True
        self.direct(target)
    
    def draw(self):
        if self.blit_switch == True: 
            screen.blit(self.image, self.rect)
            self.blit_switch  = False
        else: 
            self.blit_switch = False
            
    def direct(self, target):
        x_diff = target.rect.center[0] - self.rect.center[0]
        y_diff = target.rect.center[1] - self.rect.center[1]
        
        if x_diff != 0 and y_diff != 0: 
            if abs(x_diff) > abs(y_diff): 
                ratio = abs(y_diff) / abs(x_diff)
                self.x_diff = copysign(1, x_diff)
                self.y_diff = copysign(1, y_diff) * ratio
            elif abs(y_diff) > abs(x_diff): 
                ratio = abs(x_diff) / abs(y_diff)
                self.y_diff = copysign(1, y_diff)
                self.x_diff = copysign(1, x_diff) * ratio
            else: 
                self.x_diff = copysign(1, x_diff)
                self.y_diff = copysign(1, y_diff)
        else: 
            if x_diff == 0 and y_diff == 0: 
                self.x_diff = 0 
                self.y_diff = 0
            elif x_diff == 0: 
                self.x_diff = 0 
                if y_diff < 0: 
                    self.y_diff = -1 
                else: 
                    self.y_diff = 1
            else: 
                self.y_diff = 0
                if x_diff < 0 :
                    self.x_diff = -1
                else: 
                    self.x_diff  = 1
            
    def fade(self): 
        
        if self.alpha <= 0: 
            self.kill()
        
        self.image.fill((0, 0, self.alpha))
        self.alpha = self.alpha - 1.25
        
        
        


        

bounds = 1000
num_ants = 200

running = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([bounds, bounds])
all_ants = pygame.sprite.Group()
all_foods = pygame.sprite.Group()
activeFood = Food(50)
nest = Nest()
nests = pygame.sprite.Group()
nests.add(nest)
home_pheromones = pygame.sprite.Group()
food_pheromones = pygame.sprite.Group()


for i in range(0, num_ants): 
    ant = Ant(10, nest.rect.center)
    all_ants.add(ant) 

while running: 
    screen.fill((255, 255, 255))
    nest.draw()
    
    for pher in food_pheromones.sprites(): 
        pher.fade()
        
    for pher in home_pheromones.sprites(): 
        pher.fade()
        
    
    for ant in all_ants.sprites(): 
        ant.update()
        
        ####produce the various types of pheromones
        if ant.carry == 0 and ant.pher_delay == 0:
            home_pheromones.add(Pheromone(ant.size/3, ant.rect.center, nest))
            print("two")
        if ant.carry == 1 and ant.pher_delay == 0: 
            print("twee")
            food_pheromones.add(Pheromone(ant.size/3, ant.rect.center, ant.food_location))
        ant.pher_prod()
                                          
        #### sense the pheromones
        if ant.carry == 0 and pygame.sprite.spritecollideany(ant, food_pheromones): 
            contact_pher = pygame.sprite.spritecollide(ant, food_pheromones, False)
            ant.dx = contact_pher[0].x_diff
            ant.dy = contact_pher[0].y_diff
        if ant.carry == 1 and pygame.sprite.spritecollideany(ant, home_pheromones): 
            contact_pher = pygame.sprite.spritecollide(ant, home_pheromones, False)
            ant.dx = contact_pher[0].x_diff
            ant.dy = contact_pher[0].y_diff
            
        if pygame.sprite.spritecollideany(ant, all_foods): 
            for food in all_foods.sprites(): 
                if food.rect.colliderect(ant) and ant.carry == 0: 
                    food.shrink()
                    ant.collide()
                    ant.food_locate(food)
                    
                    
        if ant.carry == 1 and pygame.sprite.spritecollideany(ant, nests): 
            ant.dropoff()
           
            
    activeFood.cursor_move()
    all_foods.draw(screen)   
    all_ants.draw(screen)
    food_pheromones.draw(screen)
    home_pheromones.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            tempFood = Food(50)
            tempFood.hold()
            all_foods.add(tempFood)
            

    pygame.display.update()
    clock.tick(100)
pygame.quit()

