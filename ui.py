import pygame
import button
import globals
import screen

title_background = pygame.image.load("assets/title.png")
title_text = pygame.surface.Surface(screen.window_size)
title_text_lines = ["Five", "Nights", "at Freddy’s:", "Sudoku"]

shah_logo = pygame.image.load("assets/logosmall.png")

tutorial_texts = [
        [ 

         "Low on money, you took this part time job working",
         "at Five Night\'s at Freddy\'s Pizzeria.",
         "That was until the lights outside your office went", 
         "out, and a musicbox begun to chime.",
         "The exit locked, and a your computer lit up with a", 
         "sudoku puzzle. ",
         "You must solve the sudoku puzzle quickly, to make",
         "your exit before your power runs out, while also ",
         "making sure, the animatronics do not catch you.",
        "",
         "This game is best experienced with volume on."
        ],
        [
        "Use arrow keys, WASD or mouse cursor to move between", 
        "tiles in the sudoku grid.",
        "",
        "Press an number key to place it in that slot.",
        "Press backspace to remove numbers.",
        "",
        "Squares highlighted in white are part of the puzzle", 
        "and cannot be changed",
        "",
        "If a row, column or 3x3 square is highlighted red,", 
        "there is an error in your solution. ",
        ],
        [
        "To close the doors and stop animatronics, use the",
        "mouse to press the red buttons you.", 
        "",
        "If you leave them too long, you will get caught.", 
        ],
        [
        "In multiplayer mode, 2, 3 or 4 players participate.",
        "Each player gets a full round of trying to survive", 
        "the game.",
        "",
        "If nobody survives then the player that lasted the", 
        "longest will be declared the winner.",
        "If one person solves the puzzle then they will win",
        "",
        "If multiple players complete the puzzle then", "whoever did it in the least amount of time will win.",
        ]
]


#""





def draw_title_background():
    screen.screen.blit(title_background, (0, 0))


def ask(question: str, inputs: list[str], title_decoration=False) -> str:
    ask_buttons: list[button.Button] = []
    start_y = 165
    gap = 40
    ask_pos = pygame.Vector2(16, 16)
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
                return "_quit"

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
                rendered_font = globals.title_font.render(
                    line, True, globals.defaultFontColor
                )
                screen.screen.blit(rendered_font, (x_position, 40 * i))
                i += 1
            screen.screen.blit(shah_logo, (16, 280))
        pygame.display.flip()
        screen.clock.tick(60)

    return result


def announce(text: list[str], tutorial = False):
    # Milliseconds announcing the text for
    announcing = 3500

    line_count = text.__len__()
    rendered_texts = []
    rendered_positions = []
    for i in range(line_count):
        rendered_text = globals.button_font.render(
            text[i], True, globals.defaultFontColor
        )
        rendered_text_position = pygame.Vector2(0, 0)

        if tutorial:
            rendered_text_position.x = 8
            rendered_text_position.y = rendered_text.get_height() * i
        else:
            rendered_text_position.y = (
                screen.screen.get_height() - rendered_text.get_height()
            ) / 2 + rendered_text.get_height() * i
            rendered_text_position.x = (
                screen.screen.get_width() - rendered_text.get_width()
            ) / 2

        rendered_texts.append(rendered_text)
        rendered_positions.append(rendered_text_position)

    while announcing > 0:
        screen.screen.fill((0, 0, 0))

        # Handle closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "_quit"
            elif tutorial and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return -1
                elif event.key == pygame.K_RIGHT:
                    return 1

        # Draw the question
        for line in range(line_count):
            screen.screen.blit(rendered_texts[line], rendered_positions[line])

        pygame.display.flip()
        screen.clock.tick(60)
        if not tutorial:
            announcing -= screen.clock.get_time()


def tutorial():
    page = 0

    page_count = tutorial_texts.__len__()
    while page < page_count:
        page_text = [
                "<- Left arrow           " + str(page + 1) + "/" + str(page_count) + "           Right Arrow ->",
                ""
                ]

        page_text.extend(tutorial_texts[page])

        move = announce(page_text, True)
        if move == -1:
            page -= 1
        else:
            page += 1
        if page < 0:
            page = 0




