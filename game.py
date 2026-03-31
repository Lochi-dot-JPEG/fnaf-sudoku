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


skipped_player = False


# Exits the game to the title screen if accept your fate is pressed, otherwise unpause
def pause_game():
    options = ["Continue", "Accept your fate..."]

    multiplayer = globals.player_count > 1
    if multiplayer:
        options.append("Cut the power (skip player)")
    match ui.ask("Game Paused", options):
        case "Accept your fate...":
            globals.returning_to_title = True
        case "Cut the power (skip player)":
            global skipped_player
            skipped_player = True
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


def draw_power_display():
    total_seconds = (globals.max_time - globals.survival_time) / 1000
    seconds = floor(total_seconds % 60)
    minutes = floor(total_seconds / 60)

    power_label = globals.time_font.render(
        str(minutes) + " mins " + str(seconds) + " seconds of power remaining",
        1,
        globals.defaultFontColor,
    )
    screen.screen.blit(power_label, (8, 6))


def play() -> Result:

    pygame.mixer_music.load(globals.ambient_music_path)
    pygame.mixer_music.play(-1)
    # Survival time stored in milliseconds
    globals.survival_time = 0
    # Whether the player was caught throughout the game
    survived = False
    # Whether the game should loop for another frame
    playing = True

    sudoku.initialise_board()
    horror.new_game()

    while playing:
        handle_input()

        # Ends the round if returned to title from the pause menu
        if globals.returning_to_title:
            playing = False
            continue

        # Runs out of time
        global skipped_player
        if skipped_player or globals.survival_time > globals.max_time:
            skipped_player = False
            ui.announce(["You ran out of power..."])
            horror.jumpscare(False, False)
            survived = False
            playing = False
            continue

        # Checks if the horror module declares the player as caught
        if horror.caught != "":
            if horror.caught == "left":
                horror.jumpscare(True)
            if horror.caught == "right":
                horror.jumpscare(False)
            survived = False
            playing = False
            ui.announce(["You got caught..."])
            continue

        # Checks if the puzzle has been solved
        if sudoku.completed:
            survived = True
            playing = False
            ui.announce(["You Survived the Night"])
            continue

        horror.update(1.0 / 60.0)

        # Draw frame
        horror.draw_game_background()
        horror.draw_animatronics()
        sudoku.draw_board(screen.screen)
        if globals.difficulty == "Nightmare":
            horror.draw_flashlight()
        draw_power_display()

        # Draw shadow for nightmare mode

        pygame.display.flip()  # update the display
        screen.clock.tick(60)  # limits FPS to 60

        # Incremement survival time
        globals.survival_time += screen.clock.get_time()

    # Pass game result to the return of the function
    result = Result()
    result.survived = survived
    result.time = globals.survival_time
    return result
