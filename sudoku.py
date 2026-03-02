import pygame

# 2 dimensional list that stores the state of the board, with each
board_state = [
        [0,1,0,2,0,0,0,0,0],
        [0,0,0,0,3,0,0,0,0],
        [0,0,0,0,0,4,0,0,0],
        [0,0,0,0,0,0,5,0,0],
        [0,0,0,5,0,0,0,6,0],
        [0,0,0,0,0,0,0,0,7],
        [8,0,0,0,0,0,0,0,0],
        [0,9,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
]

tile_font_draw_offset = (5,0)

# Load font to draw numbers with
pygame.init()
#font = pygame.font.Font('assets/dejavu-sans/ttf/DejaVuSansMono-Bold.ttf', 20)
font = pygame.font.Font('assets/JetBrainsMonoNL-Bold.ttf', 16)


# The size of each small tile where numbers are entered
grid_tile_size = 20
# The gap between each set of three grid squares
large_gap = 4
# The gap between each grid square
small_gap = 1

large_grid_size = grid_tile_size * 3 + large_gap + small_gap * 2

board_length = grid_tile_size * 9 + large_gap * 2 + small_gap * 6

board_texture_size = (board_length, board_length)

# A pygame surface to store the texture of the rendered sudoku board
board_texture = pygame.Surface(board_texture_size)
tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))
selected_tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))

# Colours

tile_texture.fill(pygame.Color(255,255,255))
selected_tile_texture.fill(pygame.Color(200,200,200))
board_texture.fill(pygame.Color(128,128,128)) # Fill with red to test visibilty
text_color = pygame.Color(0,0,0)

# Selected tile coordinate in the grid ranging from 0-8
# Initial values are 4 to center
selected_tile_x = 4
selected_tile_y = 4


def draw_board(screen : pygame.Surface):
    center = (screen.get_width()/2,screen.get_height() / 2 )
    origin = (int(center[0] - board_length / 2), int(center[1] - board_length / 2))

    # Draw the large grid areas
    # Cycle through the x coordinates from 0-2
    for x in range(3):
        # Cycle through the y coordinates from 0-2
        for y in range(3):
            draw_3x_grid(x,y)

    screen.blit(board_texture, origin)


def draw_3x_grid(x,y):
    x_origin = x * large_grid_size
    y_origin = y * large_grid_size


    for tile_x in range(3):
        for tile_y in range(3):
            total_x_position = tile_x + x * 3 
            total_y_position = tile_y + y * 3 

            draw_location = (x_origin + tile_x * (grid_tile_size + small_gap), y_origin + tile_y * (grid_tile_size + small_gap))
            if total_x_position == selected_tile_x and total_y_position == selected_tile_y:
                board_texture.blit(selected_tile_texture, draw_location)
            else:
                board_texture.blit(tile_texture, draw_location)

            tile_text = board_state[total_y_position][total_x_position]
            if tile_text != 0:
                text_location_x = draw_location[0]
                text_location_y = draw_location[1]
                text_location_x += tile_font_draw_offset[0]
                text_location_y += tile_font_draw_offset[1]

                # This could be optimised to store the text surfaces so they do not need to be re-rendered every frame
                rendered_text = font.render(str(tile_text),True,text_color) 
                board_texture.blit(rendered_text, (text_location_x, text_location_y))

def up_pressed():
    global selected_tile_y # Allow writing to variable inside the function
    selected_tile_y -= 1
    if selected_tile_y < 0:
        selected_tile_y = 0


def down_pressed():
    global selected_tile_y # Allow writing to variable inside the function
    selected_tile_y += 1
    if selected_tile_y > 8:
        selected_tile_y = 8


def left_pressed():
    global selected_tile_x # Allow writing to variable inside the function
    selected_tile_x -= 1
    if selected_tile_x < 0:
        selected_tile_x = 0


def right_pressed():
    global selected_tile_x # Allow writing to variable inside the function
    selected_tile_x += 1
    if selected_tile_x > 8:
        selected_tile_x = 8

def key_pressed(event):
    if event.key == pygame.K_LEFT:
        left_pressed()
    elif event.key == pygame.K_RIGHT:
        right_pressed()
    elif event.key == pygame.K_UP:
        up_pressed()
    elif event.key == pygame.K_DOWN:
        down_pressed()
    elif event.key == pygame.K_1:
        input_number(1)
    elif event.key == pygame.K_2:
        input_number(2)
    elif event.key == pygame.K_3:
        input_number(3)
    elif event.key == pygame.K_4:
        input_number(4)
    elif event.key == pygame.K_5:
        input_number(5)
    elif event.key == pygame.K_6:
        input_number(6)
    elif event.key == pygame.K_7:
        input_number(7)
    elif event.key == pygame.K_8:
        input_number(8)
    elif event.key == pygame.K_9:
        input_number(9)


def input_number(value):
    board_state[selected_tile_y][selected_tile_x] = value
    
