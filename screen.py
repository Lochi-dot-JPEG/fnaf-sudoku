import pygame 

clock = pygame.time.Clock()

window_size = (640,360)
flags = pygame.SCALED | pygame.RESIZABLE #| pygame.FULLSCREEN

screen = pygame.display.set_mode(window_size, flags)
screen_rect = screen.get_rect()
pygame.display.set_caption("FNAF Sudoku")

