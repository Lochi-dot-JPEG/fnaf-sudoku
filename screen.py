import pygame 

# Pygame clock used to pause between frames
clock = pygame.time.Clock()
# Internal resolution that the game is rendered at
window_size = (640,360)
# Flags to pass to pygame window, defining that it can be resized, and will scale itself to the window size
flags = pygame.SCALED | pygame.RESIZABLE
# Game window
screen = pygame.display.set_mode(window_size, flags)
# Rectangle defining the size of the screen
screen_rect = screen.get_rect()
# The title that displays on the window
pygame.display.set_caption("FNAF Sudoku")

