import pygame

# Initialises pygame across the whole project, needed to import fonts
pygame.init()

defaultFontColor = (153, 185, 207)
locked_tile_colour = (76, 83, 95)
default_tile_colour = (42, 49, 54)
selected_tile_colour = (170, 202, 224)
board_background_color = (153, 185, 207)
error_tile_color = (140, 40, 57)
selected_tile_alpha = 60
difficulty: str = "Normal"

max_time = 60 * 10 * 1000

tile_text_color = (170, 202, 224)
tile_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 16)
button_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 20)
time_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 12)
title_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 32)

returning_to_title: bool = False
