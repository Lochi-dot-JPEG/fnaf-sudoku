import pygame
import button
import globals
import screen

title_background = pygame.image.load("assets/title.png")
title_text = pygame.surface.Surface(screen.window_size)
title_text_lines = ["Five", "Nights", "at Freddy’s:", "Sudoku"]

shah_logo = pygame.image.load("assets/logosmall.png")
def draw_title_background():
    screen.screen.blit(title_background, (0,0))

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
        screen.clock.tick(60)

    return result

def announce(text : list[str]):
    announcing = 5000

    line_count = text.__len__()
    rendered_texts = []
    rendered_positions = []
    for i in range(line_count):

        rendered_text = globals.button_font.render(text[i], True, globals.defaultFontColor)
        rendered_text_position = pygame.Vector2(0,0)
        rendered_text_position.x = (screen.screen.get_width() - rendered_text.get_width()) / 2
        rendered_text_position.y = (screen.screen.get_height() - rendered_text.get_height()) / 2 + rendered_text.get_height() * i

        rendered_texts.append(rendered_text)
        rendered_positions.append(rendered_text_position)

    while announcing > 0:
        if not pygame.mouse.get_pressed()[0]:
            can_click = True

        screen.screen.fill((0,0,0))
        screen.screen.blit(title_background, (100,0))

        # Handle closing the window
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                announcing = 0
            if event.type == pygame.QUIT:
                    pygame.quit()
                    return("_quit")

        # Draw the question
        for line in range(line_count):
            screen.screen.blit(rendered_texts[line], rendered_positions[line])

        pygame.display.flip()
        screen.clock.tick(60)
        announcing -= screen.clock.get_time()

