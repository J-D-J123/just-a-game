import pygame
from pygame.locals import *
from pygame.sprite import Group

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 464
screen_height = 615

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird v1.0.0")

# Game variables 
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

bg = pygame.image.load("FB/img/bg.png")
ground_img = pygame.image.load("FB/img/ground.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.images  = []
        self.index   = 0
        self.counter = 0

        for num in range(1, 4):
            img = pygame.image.load(f"FB/img/bird{num}.png")
            self.images.append(img)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0

    def update(self): 

        if flying == True: 
            # gravity sucks -- reality ig
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 5
            if self.rect.bottom < 500 :
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.clicked = True
                self.vel     = -10
            if pygame.mouse.get_pressed()[0] == 0: 
                self.clicked = False

            # handle the animation 
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown: 
                self.counter = 0
                self.index  += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate bird 
            self.image = pygame.transform.rotate(self.images[self.index], self.vel)
        else: 
            self.image = pygame.transform.rotate(self.images[self.index], 180)



bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# While running
run = True
while run: 
    clock.tick(fps)

    # Draw background 
    screen.blit(bg, (0, 0))

    # Draw bird
    bird_group.draw(screen)
    bird_group.update()

    # check bird is touching ground aka has died
    if flappy.rect.bottom > 500:
        game_over = True
        flying    = False


    if game_over == False: 
        # Draw and scroll the ground
        screen.blit(ground_img, (ground_scroll, 500))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
