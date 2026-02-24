import pygame


board_texture_size = (10,10) # Placeholder pixel count

# A pygame surface to store the texture of the rendered sudoku board
boards_texture = pygame.Surface(board_texture_size)

boards_texture.fill(pygame.Color(255,0,0)) # Fill with red to test visibilty

