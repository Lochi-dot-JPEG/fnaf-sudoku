import pygame
import button
import globals
import screen

# Load title screen background image
title_background = pygame.image.load("assets/title.png")
# String for each line of the title screen
title_text_lines = ["Five", "Nights", "at Freddy’s:", "Sudoku"]

# Load company logo image
shah_logo = pygame.image.load("assets/logosmall.png")


def draw_title_background():
    screen.screen.blit(title_background, (0, 0))


# Displays a menu with a string list of options
# Each is a button that can be clicked
# It then returns the text inside the selected button
# The title decorations flag draws the logo and title_text_lines
def ask(question: str, inputs: list[str], title_decoration=False) -> str:
    # List of buttons to be displayed
    ask_buttons: list[button.Button] = []

    # Variables that control the positions of buttons
    buttons_origin_y = 165
    buttons_origin_x = 16
    button_gap = 40

    # Position to draw the question text from
    question_position = pygame.Vector2(16, 16)

    # Render the question to a surface
    ask_text = globals.button_font.render(question, True, globals.defaultFontColor)

    # Create button instances for each question
    for i in range(inputs.__len__()):
        # Position of each button takes the button's index and multiplies it by the gap to space them
        button_position = pygame.Vector2(
            buttons_origin_x, buttons_origin_y + button_gap * i
        )
        label = inputs[i]
        new_button = button.Button(button_position, label)
        ask_buttons.append(new_button)

    # The text of the clicked button
    result = ""
    # Blocks checking for clicks
    can_click = False
    while result == "":
        # Allows clicking if the mouse button is detected as unpressed
        if not pygame.mouse.get_pressed()[0]:
            can_click = True

        # Handle closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        draw_title_background()

        # Update and draw each button
        for b in ask_buttons:
            b.update_clicked()
            b.draw(screen.screen)

            # If clicking is not disabled and the button is pressed
            if can_click:
                if b.pressed:
                    # set the result to button text and break out of the while loop
                    result = b.text
            else:
                b.pressed = False

        # Draw the question
        screen.screen.blit(ask_text, question_position)

        # If this is the title screen, draw the game name and Shah Corporation logo
        if title_decoration:
            i = 0
            for line in title_text_lines:
                rendered_font = globals.title_font.render(
                    line, True, globals.defaultFontColor
                )
                screen.screen.blit(rendered_font, (buttons_origin_x, 40 * i))
                i += 1
            screen.screen.blit(shah_logo, (16, 280))

        pygame.display.flip()  # Update the display
        screen.clock.tick(60)  # Limits FPS to 60

    # Returns the text of the clicked button
    return result


# Announcement function that shows text centered on a black background for 3 seconds
# The tutorial flag stops the time limit
# It instead returns either 1 or -1 if left or right arrow keys are pressed.
def announce(text: list[str], tutorial=False):
    # Milliseconds announcing the text for
    announcing = 3000

    line_count = text.__len__()
    # List to store each rendered line
    rendered_texts = []
    # List to store each rendered line's position on the screen
    rendered_positions = []
    for i in range(line_count):
        rendered_text = globals.button_font.render(
            text[i], True, globals.defaultFontColor
        )
        rendered_text_position = pygame.Vector2(0, 0)

        # Sets text to start from higher during tutorials.
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

        pygame.display.flip()  # Update the display
        screen.clock.tick(10)  # Limits FPS to 60

        # Tick down the time spent a
        if not tutorial:
            announcing -= screen.clock.get_time()


def tutorial():
    page = 0
    page_count = globals.tutorial_texts.__len__()

    while page < page_count:
        # Create top ui text for the tutorial page
        page_text = [
            "<- Left arrow           "
            + str(page + 1)
            + "/"
            + str(page_count)
            + "           Right Arrow ->",
            "",
        ]

        # Append each line of the current page of the tutorial to the page text list
        page_text.extend(globals.tutorial_texts[page])

        move = announce(page_text, True)
        if move == -1:
            page -= 1
        else:
            page += 1
        if page < 0:
            page = 0
