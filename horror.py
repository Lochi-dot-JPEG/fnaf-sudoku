import screen
import pygame
import random

background = pygame.image.load("assets/office.png")
left_door_pos = pygame.Vector2(41,69)
left_animatronic_pos = pygame.Vector2(41,89)
left_animatronic_image = pygame.image.load("assets/bonnie.png")
left_door_image = pygame.image.load("assets/doorleft.png")
left_door_close = 1.0

right_door_pos = pygame.Vector2(529,89)
right_animatronic_pos = pygame.Vector2(529,89)
right_animatronic_image = pygame.image.load("assets/freddy.png")
right_door_image = pygame.image.load("assets/doorright.png")
right_door_close = 1.0

door_close_length = 5.0
animatronic_max_distance = 120
animatronic_min_distance = 30

default_background_rect = screen.screen_rect 

# The amount of pixels on the border of the background along the y axis
background_padding_y = int((background.get_height() - screen.screen_rect.height)/2)

# The amount of pixels on the border of the background along the x axis
background_padding_x = int((background.get_width() - screen.screen_rect.width)/2)

default_background_rect.x -= background_padding_x
default_background_rect.y -= background_padding_y

# Amount of pixel the mouse has to move to pan the background by 1 pixel, negative values reverse direction of movement
background_pan = -20

left_animatronic_distance = 15
right_animatronic_distance = 5

# Amount of seconds given to notice the animatronic before you lose
animatronic_warning_time = 15

background_draw_offset = pygame.Vector2(0,0)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def draw_game_background():
    global background_draw_offset

    mouse_offset_from_center_x = (screen.pygame.mouse.get_pos()[0]- screen.screen_rect.width/2)
    mouse_offset_from_center_y = (screen.pygame.mouse.get_pos()[1]- screen.screen_rect.height/2)
    print(mouse_offset_from_center_x)
    print(mouse_offset_from_center_y)

    # Convert to integer because drawing rectangles only use full pixels and store their values as int
    offset_bg_x = int(mouse_offset_from_center_x / background_pan)
    offset_bg_y = int(mouse_offset_from_center_y / background_pan)
    offset_bg_x = clamp(offset_bg_x, -background_padding_x, background_padding_x)
    offset_bg_y = clamp(offset_bg_y, -background_padding_y, background_padding_y)

    background_draw_offset.x = offset_bg_x
    background_draw_offset.y = offset_bg_y

    # Prevent the background from panning outside of the edge of the image
    screen.screen.blit(background, background_draw_offset)

def update(delta : float):
    global left_animatronic_distance 
    global right_animatronic_distance 
    global left_door_close 
    global right_door_close 
    left_animatronic_distance -= delta
    left_door_close -= delta
    right_door_close -= delta
    right_animatronic_distance -= delta
    

def close_door_left():
    global left_door_close
    global left_animatronic_distance
    left_door_close = door_close_length
    left_animatronic_distance = random.randrange(animatronic_min_distance, animatronic_max_distance)


def close_door_right():
    global right_door_close
    global right_animatronic_distance
    right_door_close = door_close_length
    right_animatronic_distance = random.randrange(animatronic_min_distance, animatronic_max_distance)



def draw_animatronics():
    if left_door_close > 0:
        screen.screen.blit(left_door_image, left_door_pos + background_draw_offset)
    elif left_animatronic_distance < animatronic_warning_time:
        alpha = 255 - int((left_animatronic_distance / animatronic_warning_time) * 255)
        left_animatronic_image.set_alpha(alpha)
        screen.screen.blit(left_animatronic_image, left_animatronic_pos + background_draw_offset)

    if right_door_close > 0:
        screen.screen.blit(right_door_image, right_door_pos + background_draw_offset)
    elif right_animatronic_distance < animatronic_warning_time:
        alpha = 255 - int((right_animatronic_distance / animatronic_warning_time) * 255)
        left_animatronic_image.set_alpha(alpha)
        screen.screen.blit(right_animatronic_image, right_animatronic_pos+ background_draw_offset)



