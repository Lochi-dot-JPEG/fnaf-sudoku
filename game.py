import sudoku
import pygame
import button
import globals
import horror
import screen


title_background = pygame.image.load("assets/title.png")
title_text = pygame.surface.Surface(screen.window_size)
title_text_lines = ["Five", "Nights", "at Freddy’s:", "Sudoku"]
shah_logo = pygame.image.load("assets/logosmall.png")

clock = pygame.time.Clock()

class Result:
    survived = True
    # Amount of time the game ran
    # For survivors this is how long it took to complete the puzzle
    # For deaths it is how long they survived
    time = 0.0

def draw_title_background():
    screen.screen.blit(title_background, (0,0))




def handle_input():
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            used = sudoku.click_tile(screen.screen)
            if not used:
                horror.click()

        elif event.type == pygame.KEYDOWN:
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

    sudoku.initialise_board()
    while playing:
        handle_input()
        horror.update(1.0/60.0)
        horror.draw_game_background()
        horror.draw_animatronics()
        sudoku.draw_board(screen.screen)
        pygame.display.flip() # update the display
        clock.tick(60)  # limits FPS to 60

    # Pass game result to the return of the function
    result = Result()
    result.survived = survived
    result.time = survival_time
    return result




def ask(question: str, inputs: list[str], title_decoration = False) -> str:
    ask_buttons : list[button.Button] = []
    start_y = 165
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

        # Handle closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    return("_quit")

        for b in ask_buttons:
            b.update_hover()
            b.draw(screen.screen)

            if can_click:
                if b.pressed:
                    result = b.text
            else:
                b.pressed = False

        # Draw the question
        screen.screen.blit(ask_text, ask_pos)

        if title_decoration:
            i = 0
            for line in title_text_lines:
                rendered_font = globals.title_font.render(line, True, globals.defaultFontColor)
                screen.screen.blit(rendered_font, (x_position,40 * i))
                i += 1
            screen.screen.blit(shah_logo, (16, 280))
        pygame.display.flip()
        clock.tick(60)

    return result

