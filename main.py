
import pygame
import sudoku_scene

# pygame setup
pygame.init()
running = True
window_size = (640,360)
clock = pygame.time.Clock()
flags = pygame.SCALED | pygame.RESIZABLE #| pygame.FULLSCREEN
screen = pygame.display.set_mode(window_size, flags)
pygame.display.set_caption("FNAF Sudoku")
screen_rect = screen.get_rect()

background = pygame.image.load("assets/office.png")

default_background_rect = screen.get_rect() # TODO change to only store the x and y positions because height and width are ignored

# The amount of pixels on the border of the background along the y axis
background_padding_y = int((background.get_height() - screen_rect.height)/2)

# The amount of pixels on the border of the background along the x axis
background_padding_x = int((background.get_width() - screen_rect.width)/2)

default_background_rect.x -= background_padding_x
default_background_rect.y -= background_padding_y
# Amount of pixel the mouse has to move to pan the background by 1 pixel, negative values reverse direction of movement
background_pan = -20

def draw_background():
    draw_rect = default_background_rect.copy()

    mouse_offset_from_center_x = (pygame.mouse.get_pos()[0]- screen_rect.width/2)
    mouse_offset_from_center_y = (pygame.mouse.get_pos()[1]- screen_rect.height/2)

    # Convert to integer because drawing rectangles only use full pixels and store their values as int
    offset_bg_x = int(mouse_offset_from_center_x / background_pan)
    offset_bg_y = int(mouse_offset_from_center_y / background_pan)
    offset_bg_x = clamp(offset_bg_x, -background_padding_x, background_padding_x)
    offset_bg_y = clamp(offset_bg_y, -background_padding_y, background_padding_y)

    draw_rect.x += offset_bg_x
    draw_rect.y += offset_bg_y

    # Prevent the background from panning outside of the edge of the image
    screen.blit(background, draw_rect)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    draw_background()

    sudoku_scene.draw_board(screen)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
