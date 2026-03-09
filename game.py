import sudoku
import pygame
import button
import globals

window_size = (640,360)
clock = pygame.time.Clock()
flags = pygame.SCALED | pygame.RESIZABLE #| pygame.FULLSCREEN
screen = pygame.display.set_mode(window_size, flags)
pygame.display.set_caption("FNAF Sudoku")
screen_rect = screen.get_rect()

background = pygame.image.load("assets/office.png")
title_background = pygame.image.load("assets/title.png")
title_text = pygame.surface.Surface(window_size)
title_text_lines = ["Five", "Nights", "at Freddy’s:", "Sudoku"]

default_background_rect = screen.get_rect() # TODO change to only store the x and y positions because height and width are ignored

# The amount of pixels on the border of the background along the y axis
background_padding_y = int((background.get_height() - screen_rect.height)/2)

# The amount of pixels on the border of the background along the x axis
background_padding_x = int((background.get_width() - screen_rect.width)/2)

default_background_rect.x -= background_padding_x
default_background_rect.y -= background_padding_y
# Amount of pixel the mouse has to move to pan the background by 1 pixel, negative values reverse direction of movement
background_pan = -20

class Result:
    survived = True
    # Amount of time the game ran
    # For survivors this is how long it took to complete the puzzle
    # For deaths it is how long they survived
    time = 0.0

def draw_title_background():
    screen.blit(title_background, (0,0))

def draw_game_background():
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

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            sudoku.key_pressed(event)

        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def play() -> Result:
    survival_time = 0.0
    survived = False
    # Whether the game should loop for another frame
    playing = True

    while playing:
        handle_input()
        # fill the screen with a color to wipe away anything from last frame

        draw_game_background()
        sudoku.draw_board(screen)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60



    # Pass game result to the return of the function
    result = Result()
    result.survived = survived
    result.time = survival_time
    return result



def show_title(inputs: list[str]) -> str:
    result = ask("", inputs, True)
    return result


def ask(question: str, inputs: list[str], title_decoration = False) -> str:
    ask_buttons : list[button.Button] = []
    start_y = 220
    gap = 40
    ask_pos = pygame.Vector2(16,16)
    x_position = 16
    ask_text = globals.button_font.render(question, True, globals.defaultFontColor)

    for i in range(inputs.__len__()):
        button_position = pygame.Vector2(x_position, start_y + gap * i)
        label = inputs[i] 
        new_button = button.Button(button_position, label)
        ask_buttons.append(new_button)

    result = ""
    # Where the result is stored while waiting for the player to release the mouse button
    can_click = False
    while result == "":
        if not pygame.mouse.get_pressed()[0]:
            can_click = True
        draw_title_background()

        # TODO wrap this in a separate function that doesnt interfere with grid code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    return("_quit")
                    
        for b in ask_buttons:
            b.draw(screen)

            if can_click:
                if b.pressed:
                    result = b.text
            else:
                b.pressed = False


        screen.blit(ask_text, ask_pos)
        if title_decoration:
            i = 0
            for line in title_text_lines:
                rendered_font = globals.title_font.render(line, True, globals.defaultFontColor)
                screen.blit(rendered_font, (x_position,48 * i))
                i += 1

        pygame.display.flip()
        clock.tick(60)


    return result

