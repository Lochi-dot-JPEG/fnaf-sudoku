import screen
import pygame

background = pygame.image.load("assets/office.png")

default_background_rect = screen.screen_rect 

# The amount of pixels on the border of the background along the y axis
background_padding_y = int((background.get_height() - screen.screen_rect.height)/2)

# The amount of pixels on the border of the background along the x axis
background_padding_x = int((background.get_width() - screen.screen_rect.width)/2)

default_background_rect.x -= background_padding_x
default_background_rect.y -= background_padding_y

# Amount of pixel the mouse has to move to pan the background by 1 pixel, negative values reverse direction of movement
background_pan = -20

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def draw_game_background():
    draw_rect = default_background_rect.copy()

    mouse_offset_from_center_x = (screen.pygame.mouse.get_pos()[0]- screen.screen_rect.width/2)
    mouse_offset_from_center_y = (screen.pygame.mouse.get_pos()[1]- screen.screen_rect.height/2)
    print(mouse_offset_from_center_x)
    print(mouse_offset_from_center_y)

    # Convert to integer because drawing rectangles only use full pixels and store their values as int
    offset_bg_x = int(mouse_offset_from_center_x / background_pan)
    offset_bg_y = int(mouse_offset_from_center_y / background_pan)
    offset_bg_x = clamp(offset_bg_x, -background_padding_x, background_padding_x)
    offset_bg_y = clamp(offset_bg_y, -background_padding_y, background_padding_y)

    draw_rect.x += offset_bg_x
    draw_rect.y += offset_bg_y

    # Prevent the background from panning outside of the edge of the image
    screen.screen.blit(background, draw_rect)
