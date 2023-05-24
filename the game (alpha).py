#import library
import pygame
from pygame.locals import *
import sys
import random

#initialize pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

#window dimensions
screen_w = 500
screen_h = 720

#create window
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Dumpster Dash')

#scrolling background
bg_image = pygame.image.load('assets/bg.png').convert()
overlap_bg_image = pygame.image.load('assets/bg.png').convert()
b_pos = 0
o_pos = 720
speed = 7

#lane coordinates
left_lane = 150
center_lane = 166
right_lane = 275  
lanes = [left_lane, center_lane, right_lane]

objectleft_lane= 130
objectcenter_lane= 245
objectright_lane= 360
objectlanes = [objectleft_lane, objectcenter_lane, objectright_lane]

# Height
height = 500

#wally
class Runner:
    def __init__(self, x, y, animation_list):
        self.alive = True
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        animation_cooldown = 20
        #handle animation
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
        #if the animation surpasses last frame, reset
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
    def draw(self):
        screen.blit(self.image, self.rect)

class Bio(Runner):
    def __init__(self, x, y):
        animation_list = []
        for i in range(16):
            img = pygame.image.load(f'assets/wallyrunbio/{i}.png')
            animation_list.append(img)
        super().__init__(x, y, animation_list)
        
class NonBio(Runner):
    def __init__(self, x, y):
        animation_list = []
        for i in range(16):
            img = pygame.image.load(f'assets/wallyrunnonbio/{i}.png')
            animation_list.append(img)
        super().__init__(x, y, animation_list)

wally1 = Bio(250, 575)
wally2 = NonBio(250, 575)

active_wally = wally1
prev_wally_position = active_wally.rect.center

player_group = pygame.sprite.Group
bio_group = pygame.sprite.Group
nonbio_group = pygame.sprite.Group


class Garbage(pygame.sprite.Sprite):
        def __init__(self, image, x, y,):
            pygame.sprite.Sprite.__init__(self)
        
  # scale the image down so it's not wider than the lane
            image_scale = 100 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            
class BioGarbage(Garbage):
    pass

class NonBioGarbage(Garbage):
    pass
            
# Sprite groups
garbage_group = pygame.sprite.Group()

# Load the garbage images
gar1 = BioGarbage
bio_filenames = ['banana peel.png', 'milk carton.png', 'box.png']
biodegradable_images = []
for bio_filename in bio_filenames:
    image = pygame.image.load('assets/' + bio_filename)
    biodegradable_images.append(image) 

gar2 = NonBioGarbage
nonbio_filenames = ['plastic bag.png', 'soda bottle.png', 'water bottle.png']
nonbiodegradable_images = []
for nonbio_filename in nonbio_filenames:
    image = pygame.image.load('assets/' + nonbio_filename)
    
    nonbiodegradable_images.append(image)


# Loop to retain screen
gamerun = True
while gamerun:
    clock.tick(FPS)  # FPS of game

    # Event Handle
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT and active_wally.rect.center[0] > left_lane:
                active_wally.rect.left -= 115
            elif event.key == K_RIGHT and active_wally.rect.center[0] < right_lane:
                active_wally.rect.left += 115
            elif event.key == K_q:
                prev_wally_position = active_wally.rect.center  # Store the current position
                active_wally = wally1
                active_wally.rect.center = prev_wally_position  # Set the position to the stored position
            elif event.key == K_e:
                prev_wally_position = active_wally.rect.center  # Store the current position
                active_wally = wally2
                active_wally.rect.center = prev_wally_position  # Set the position to the stored position
            # Quitting the Game           
            elif event.key == K_ESCAPE:
                gamerun = False
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

     # Draw scrolling background
    if b_pos >= screen_h:
        b_pos = -screen_h
    if o_pos >= screen_h:
        o_pos = -screen_h

    b_pos += speed
    o_pos += speed
   

    screen.blit(bg_image, (0, b_pos))
    screen.blit(overlap_bg_image, (0, o_pos))

    # Update and draw the active version of Wally
    active_wally.update()
    active_wally.draw()



    # Add a garbage

    # Ensure there's enough gap between garbage items
    if len(garbage_group) < 3:
        add_garbage = True
        for garbage in garbage_group:
            if garbage.rect.top < garbage.rect.height * 1:  # Closeness of spawning
                add_garbage = False

        if add_garbage:
            # Select a random lane
            lane = random.choice(objectlanes)

            garbage_list = [gar1, gar2]

            # Select a random garbage object
            garbage_object = random.choice(garbage_list)

            # Select a random garbage image
            if garbage_object == gar1:
                image = random.choice(biodegradable_images)
            else:
                image = random.choice(nonbiodegradable_images)

            # Create a new garbage object with the selected image
            garbage = garbage_object(image, lane, -height / 2)
            garbage.rect.center = (lane, -height / 2)
            garbage_group.add(garbage)

    # Move the garbage and remove it if it goes off screen
    for garbage in garbage_group:
        garbage.rect.y += speed

        # Remove garbage once it goes off screen
        if garbage.rect.top >= height:
            garbage.kill()

    # Draw the garbage
    garbage_group.draw(screen)

    # Update display window
    pygame.display.update()