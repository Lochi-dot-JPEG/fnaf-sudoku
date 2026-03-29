import pygame
import player_management
import ui
import globals

# Initialise pygame's sound mixer to enable audio
pygame.mixer.init()
# Import necessary modules

title_options = ["Play Game", "Tutorial", "Quit"]

# Play and loop music infinitely

running = True
while running:
    pygame.mixer.music.load(globals.musicbox_music_path)
    pygame.mixer.music.play()
    globals.returning_to_title = False

    # Display title screen with title decorations enabled
    selected_title_button = ui.ask("", title_options, True)

    # Handle whichever button has been pressed
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            ui.tutorial()
        case _:
            pygame.quit()
            running = False
