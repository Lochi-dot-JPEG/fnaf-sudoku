import pygame
import random
import globals

# 2 dimensional list that stores the state of the board, accessible through board_state[x][y]
board_state = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
]

monitor = pygame.image.load("assets/monitor.png")
monitor.set_colorkey((0,255,0))
locked_squares : list[tuple[int,int]]= []
completed = False

tile_font_draw_offset = (5,0)

failed_rows : list[int] = []
failed_columns : list[int] = []
failed_squares : list[pygame.Vector2] = []

# The size of each small tile where numbers are entered
grid_tile_size = 20
# The gap between each set of three grid squares
large_gap = 2
# The gap between each grid square
small_gap = 1

large_grid_size = grid_tile_size * 3 + large_gap + small_gap * 2

board_length = grid_tile_size * 9 + large_gap * 2 + small_gap * 6

board_texture_size = (board_length, board_length)

# A pygame surface to store the texture of the rendered sudoku board
board_texture = pygame.Surface(board_texture_size)
tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))
selected_tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))
error_tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))
locked_tile_texture = pygame.Surface((grid_tile_size, grid_tile_size))

tile_texture.fill(globals.default_tile_colour)
selected_tile_texture.fill(globals.selected_tile_colour)
selected_tile_texture.set_alpha(globals.selected_tile_alpha)
error_tile_texture.fill(globals.error_tile_color)
board_texture.fill(globals.board_background_color)
locked_tile_texture.fill(globals.locked_tile_colour)

# Selected tile coordinate in the grid ranging from 0-8
# Initial values are 4 to center
selected_tile_x = 4
selected_tile_y = 4


def initialise_board():
    new_state = get_random_puzzle()
    global completed
    completed = False
    global locked_squares
    locked_squares = []
    index = 0
    for y in range(9):
        for x in range(9):
            value = int(new_state[index])
            board_state[x][y] = value
            if (value != 0):
                locked_squares.append((x,y))
            index += 1

    board_changed()



def update_board_texture():
    # Draw the large grid areas
    # Cycle through the x coordinates from 0-2
    for x in range(3):
        # Cycle through the y coordinates from 0-2
        for y in range(3):
            draw_3x_grid(x,y)

    # Check if the grid is completed
    global completed 
    completed = True
    for x in range(9):
        for y in range(9):
            if board_state[x][y] == 0:
                completed = False

def click_tile(screen) -> bool:
    mouse_position = pygame.mouse.get_pos()

    origin = get_origin_on_screen(screen)
    position_on_grid = (mouse_position[0] - origin[0], mouse_position[1] - origin[1])

    hovered = (int(position_on_grid[0]/ (grid_tile_size + small_gap)), int(position_on_grid[1]/ (grid_tile_size + small_gap)))

    if hovered[0] > 8 or hovered[0] < 0:
        return False
    if hovered[1] > 8 or hovered[1] < 0:
        return False

    global selected_tile_x 
    global selected_tile_y 
    selected_tile_x = hovered[0]
    selected_tile_y = hovered[1]
    update_board_texture()
    return True


def get_origin_on_screen(screen : pygame.Surface) -> tuple[int,int]:
    center = (screen.get_width()/2,screen.get_height() / 2 )
    return (int(center[0] - board_length / 2), int(center[1] - board_length / 2))


def draw_board(screen : pygame.Surface):
    origin = get_origin_on_screen(screen)
    screen.blit(monitor, (origin[0]- 45,origin[1] - 50))
    screen.blit(board_texture, origin)


def draw_3x_grid(x,y):
    x_origin = x * large_grid_size
    y_origin = y * large_grid_size

    # Coordinate of the 3x3 square to be compared to any errors in failed_squares
    square = pygame.Vector2(x,y)
    for tile_x in range(3):
        for tile_y in range(3):
            total_x_position = tile_x + x * 3 
            total_y_position = tile_y + y * 3 

            draw_location = (x_origin + tile_x * (grid_tile_size + small_gap), y_origin + tile_y * (grid_tile_size + small_gap))


            if (total_x_position,total_y_position) in locked_squares:
                board_texture.blit(locked_tile_texture, draw_location)
            elif total_y_position in failed_rows or total_x_position in failed_columns or square in failed_squares:
                board_texture.blit(error_tile_texture, draw_location)
            else:
                board_texture.blit(tile_texture, draw_location)

            if total_x_position == selected_tile_x and total_y_position == selected_tile_y:
                board_texture.blit(selected_tile_texture, draw_location)

            tile_text = board_state[total_x_position][total_y_position]
            if tile_text != 0:
                text_location_x = draw_location[0]
                text_location_y = draw_location[1]
                text_location_x += tile_font_draw_offset[0]
                text_location_y += tile_font_draw_offset[1]

                # This could be optimised to store the text surfaces so they do not need to be re-rendered every frame
                rendered_text = globals.tile_font.render(str(tile_text),True,globals.tile_text_color) 
                board_texture.blit(rendered_text, (text_location_x, text_location_y))

def up_pressed():
    global selected_tile_y # Allow writing to variable inside the function
    selected_tile_y -= 1
    if selected_tile_y < 0:
        selected_tile_y = 0
    update_board_texture()


def down_pressed():
    global selected_tile_y # Allow writing to variable inside the function
    selected_tile_y += 1
    if selected_tile_y > 8:
        selected_tile_y = 8
    update_board_texture()


def left_pressed():
    global selected_tile_x # Allow writing to variable inside the function
    selected_tile_x -= 1
    if selected_tile_x < 0:
        selected_tile_x = 0
    update_board_texture()


def right_pressed():
    global selected_tile_x # Allow writing to variable inside the function
    selected_tile_x += 1
    if selected_tile_x > 8:
        selected_tile_x = 8
    update_board_texture()



def key_pressed(event):
# Moving selection with arrows or wasd
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        left_pressed()
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        right_pressed()
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        up_pressed()
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        down_pressed()
# Clear inputting numbers into squares
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
    elif event.key == pygame.K_BACKSPACE: # Clear grid square
        input_number(0)


def board_changed():
    global failed_rows
    global failed_columns
    global failed_squares
    failed_rows = check_rows()
    failed_columns = check_columns()
    failed_squares = check_squares()
    update_board_texture()


def check_rows() -> list[int]:
    fails = []
    for y in range(9):
        row_values = []
        for x in range(9):
            row_values.append(board_state[x][y])

        if not (0 in row_values):
            if not check_all_unique(row_values):
                fails.append(y)
    return fails


def check_columns() -> list[int]:
    fails = []
    for x in range(9):
        column_values = board_state[x]
        if not (0 in column_values):
            if not check_all_unique(column_values):
                fails.append(x)
    return fails


def check_squares() -> list[pygame.Vector2]:
    fails : list[pygame.Vector2] = []

    for square_x in range(3):
        for square_y in range(3):
            square_values = []
            for x in range(3):
                for y in range(3):
                    square_values.append(board_state[square_x * 3 + x][square_y * 3 + y])

            if not (0 in square_values):
                if not check_all_unique(square_values):
                    fails.append(pygame.Vector2(square_x, square_y))
    return fails


def check_all_unique(numbers : list[int]) -> bool:
    for i in range(1,10):
        if numbers.count(i) != 1:
            return False
    return True


def input_number(value):
    if not ((selected_tile_x, selected_tile_y) in locked_squares):
        board_state[selected_tile_x][selected_tile_y] = value
    board_changed()

def get_random_puzzle() -> str:
    lines = []

    filename = "assets/easypuzzles.txt"
    if globals.difficulty == "Hard":
        filename = "assets/hardpuzzles.txt"

    with open(filename, "r") as file:
        lines = [line.rstrip() for line in file]

    return random.choice(lines)
