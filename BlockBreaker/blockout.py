import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height= 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Block Breakout v1.0.0")

bg = (234, 218, 184)

# block colors 
block_red = (242, 85, 96)
block_green = (86,174, 87)
block_blue = (69, 177, 232)

# game variables 
cols = 6
rows = 6

# brick wall class
class wall(): 
    def __init__(self): 
        self.width = screen_width // cols
        self.height = 50 
    
    def create_wall(self):
        self.blocks = []
        # define empty list for blocks 
        block_individual = []
        for row in range(rows): 
            # reset the block list 
            block_row = [] 
            # go through the colums 
            for col in range(cols): 
                # generate x and y positions for each block and create rectangle 
                block_x = col * self.width
                block_y = row * self.height 
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign color based on row 
                if row < 2: 
                    strength = 3
                elif row < 4: 
                    strength = 2
                elif row < 6: 
                    strength = 1
                # make a list to store the block data 
                block_individual = [rect, strength]
                # append that list to the current block row 
                block_row.append(block_individual)
            # append the row to the full list of blocks 
            self.blocks.append(block_row)
    
    def draw_wall(self): 
        for row in self.blocks: 
            for block in row: 
                # assign color based on block strength 
                if block[1] == 3: 
                    block_col = block_blue
                elif block[1] == 2: 
                    block_col = block_green
                elif block[1] == 1: 
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)
                
# create a wall 
wall = wall()
wall.create_wall()

run = True
while run:

    # color the screen and then update later on 
    screen.fill(bg)

    # draw wall 
    wall.draw_wall()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False 

    pygame.display.update()

pygame.quit()