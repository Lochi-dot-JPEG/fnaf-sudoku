import pygame


grid_tile_size = 24
large_gap = 3
small_gap = 2

large_grid_size = grid_tile_size * 3 + large_gap + small_gap * 2

board_length = grid_tile_size * 9 + large_gap * 2 + small_gap * 6

board_texture_size = (board_length ,board_length)

# A pygame surface to store the texture of the rendered sudoku board
board_texture = pygame.Surface(board_texture_size)
tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))
tile_texture.fill(pygame.Color(255,255,255))

board_texture.fill(pygame.Color(128,128,128)) # Fill with red to test visibilty



def draw_board(screen : pygame.Surface, draw_position):

    # Draw the large grid areas
    for x in range(3):
        for y in range(3):
            draw_3x_grid(x * large_grid_size,y * large_grid_size)


    screen.blit(board_texture, draw_position)


def draw_3x_grid(x,y):
    for tile_x in range(3):
        for tile_y in range(3):
            board_texture.blit(tile_texture,
                               (x + tile_x * (grid_tile_size + small_gap), 
                                y + tile_y * (grid_tile_size + small_gap)
            ))

