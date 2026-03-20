from math import floor
import sudoku
import pygame
import globals
import horror
import screen
import ui


# Class storing the result of the round of a game
class Result:
    # Whether the player survived the game
    survived: bool = True
    # Amount of time the game ran
    # For survivors this is how long it took to complete the puzzle
    # For deaths it is how long they survived
    time: int = 0


# Exits the game to the title screen if accept your fate is pressed, otherwise unpause
def pause_game():
    match ui.ask("Game Paused", ["Continue", "Accept your fate..."]):
        case "Accept your fate...":
            globals.returning_to_title = True
        case _:
            pass


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            used = sudoku.click_tile(screen.screen)
            if not used:
                horror.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()
            sudoku.key_pressed(event)

        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def draw_power(survival_time: int):
    total_seconds = (globals.max_time - survival_time) / 1000
    seconds = floor(total_seconds % 60)
    minutes = floor(total_seconds / 60)

    power_label = globals.time_font.render(
        str(minutes) + " mins " + str(seconds) + " seconds power remain",
        1,
        globals.defaultFontColor,
    )
    screen.screen.blit(power_label, (8, 6))


def play() -> Result:
    # Survival time stored in milliseconds
    survival_time: int = 0
    # Whether the player was caught throughout the game
    survived = False
    # Whether the game should loop for another frame
    playing = True

    sudoku.initialise_board()
    horror.new_game()
    while playing:
        handle_input()
        if globals.returning_to_title:
            playing = False
            continue

        horror.update(1.0 / 60.0)
        horror.draw_game_background()
        horror.draw_animatronics()
        draw_power(survival_time)
        sudoku.draw_board(screen.screen)
        pygame.display.flip()  # update the display
        screen.clock.tick(60)  # limits FPS to 60
        survival_time += screen.clock.get_time()

        if survival_time > globals.max_time:
            ui.announce(["You ran out of power..."])
            horror.jumpscare(False)
            survived = False
            playing = False
        if horror.caught != "":
            if horror.caught == "left":
                horror.jumpscare(True)
            if horror.caught == "right":
                horror.jumpscare(False)
            survived = False
            playing = False
            ui.announce(["You got caught..."])
        if sudoku.completed:
            survived = True
            playing = False
            ui.announce(["You Survived the Night"])

    # Pass game result to the return of the function
    result = Result()
    result.survived = survived
    result.time = survival_time
    return result
