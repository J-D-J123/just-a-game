import pygame
import random
from pygame.locals import *
from pygame import mixer

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 464
screen_height = 615

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird v1.0.0")

# Define font
font = pygame.font.SysFont("Bauhaus 93", 60)

# Define colors
white = (255, 255, 255)

# Game variables
ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 2000  # milliseconds
score = 0
pass_pipe = False
last_pipe = pygame.time.get_ticks()

# Background music
mixer.music.load("FB/sounds/background_lofi.mp3")
mixer.music.play(-1)

# Preload images
bg = pygame.image.load("FB/img/bg.png")
ground_img = pygame.image.load("FB/img/ground.png")
bird_images = [pygame.image.load(f"FB/img/bird{num}.png") for num in range(1, 4)]
pipe_img = pygame.image.load("FB/img/pipe.png")
button_img = pygame.image.load("FB/img/restart.png")

# Game state variables
attempts_needed = 0
random_attempt_genator = random.randint(1, 5)
show_scare_image = False
scare_image_timer = 0  # To track when to show the scare image
jump_scare_played = False  # Flag to ensure jump scare sound plays only once
shake_timer = 0  # Timer to manage the shaking duration
shake_duration = 500  # Duration of the shaking effect in milliseconds
shake_intensity = 10  # Maximum pixel displacement for shaking

def draw_text(text, font, text_col, x, y): 
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Clear memory and reset game 
def reset_game(): 
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2) 
    score = 0
    return score 

def resetAttempts():
    global attempts_needed
    attempts_needed = 0

def jumpScareReset():
    global random_attempt_genator
    random_attempt_genator = random.randint(1, 5)

def resetMusic():
    # Restart background music
    mixer.music.load("FB/sounds/background_lofi.mp3")
    mixer.music.play(-1)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_images
        self.index = 0
        self.counter = 0
        self.clicked = False
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.angle = 0

    def update(self):
        if flying and not game_over:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 500:
                self.rect.y += int(self.vel)
            else:
                self.rect.bottom = 500
                self.vel = 0

        if not game_over:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -8.5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate bird
            self.image = pygame.transform.rotate(self.image, self.vel)
        else:
            if self.rect.bottom < 500:
                self.vel += 0.5
                self.rect.y += int(self.vel)
                self.angle = min(max(self.vel * -2, -90), 90)
            else:
                self.angle = 180
                self.image = pygame.transform.rotate(self.images[self.index], self.angle)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_img
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: 
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

class Button(): 
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self): 
        action = False

        # Get mouse position 
        pos = pygame.mouse.get_pos()

        # Check if mouse is over button 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Create restart button instance 
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

# While running
run = True
while run:

    clock.tick(fps)  # Ensure the game runs at the specified fps

    # Draw background
    screen.blit(bg, (0, 0))

    # Update and draw bird
    bird_group.update()
    bird_group.draw(screen)

    # Update and draw pipes
    pipe_group.update()
    pipe_group.draw(screen)
    
    if game_over:
        draw_text(str(score), font, white, int(screen_width / 2), 20)

        # Check if the scare image should be shown
        if show_scare_image and attempts_needed == random_attempt_genator:
            if not jump_scare_played:
                # Stop background music
                mixer.music.stop()
                
                # Start jump scare sound
                scarePNG = random.randint(1,19)
                print(scarePNG)

                # Jump scare image
                jumpIMG = pygame.image.load(f"FB/img/SC/{scarePNG}.jpg")

                mixer.music.load("FB/sounds/1.mp3")
                mixer.music.play()  # Play sound only once
                jump_scare_played = True 

            # Calculate shaking offset
            current_time = pygame.time.get_ticks()
            if shake_timer == 0:
                shake_timer = current_time
            
            # Duration check
            if current_time - shake_timer < shake_duration:
                x_offset = random.randint(-shake_intensity, shake_intensity)
                y_offset = random.randint(-shake_intensity, shake_intensity)
                # Scale the jump scare image to fit the screen
                scaled_jumpIMG = pygame.transform.scale(jumpIMG, (screen_width, screen_height))
                # Blit the image with shaking effect
                screen.blit(scaled_jumpIMG, (x_offset, y_offset))
            else:
                # Stop shaking
                shake_timer = 0
                screen.blit(jumpIMG, (0, 0))

        # Handle button press
        if button.draw() and attempts_needed != random_attempt_genator:
            attempts_needed += 1
            print(f"Your Score Was {score}")
            score = reset_game()
            show_scare_image = False
            game_over = False
            jump_scare_played = False  # Reset the flag for the next game
            resetMusic()  # Restart background music

        elif button.draw() and attempts_needed == random_attempt_genator: 
            resetAttempts()
            jumpScareReset() 
            print(f"Your Score Was {score}")
            score = reset_game()
            show_scare_image = False
            game_over = False
            jump_scare_played = False  # Reset the flag for the next game
            resetMusic()  # Restart background music

    else:
        # Check the score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and not pass_pipe:
                pass_pipe = True
            if pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False
        draw_text(str(score), font, white, int(screen_width / 2), 20)

        # Check for collisions and ground hit
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
            scare_image_timer = pygame.time.get_ticks()  # Start the timer

        if flappy.rect.bottom >= 500:
            game_over = True
            flying = False
            flappy.rect.bottom = 500  
            flappy.vel = 0  

    if not game_over and flying:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Draw and scroll the ground
        if not (game_over and show_scare_image and attempts_needed == random_attempt_genator):
            screen.blit(ground_img, (ground_scroll, 500))
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
    else:
        if not (game_over and show_scare_image and attempts_needed == random_attempt_genator):
            screen.blit(ground_img, (ground_scroll, 500))

    # Check if we need to show the scare image
    if game_over and not show_scare_image:
        # If enough time has passed (2 to 5 seconds)
        current_time = pygame.time.get_ticks()
        if current_time - scare_image_timer >= random.randint(2000, 5000):
            show_scare_image = True

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
