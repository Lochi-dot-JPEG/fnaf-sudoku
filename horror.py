from warnings import warn
import screen
import pygame
import random
import globals

from ui import draw_title_background

# Jumpscare sound loaded from ogg file
jumpscare_sound = pygame.mixer.Sound("assets/jumpscare.ogg")
# Door sound loaded from ogg file
door_sound = pygame.mixer.Sound("assets/door.ogg")

# Load flashlight image
flashlight_image = pygame.image.load("assets/nightmarelight.png")

# The jumpscare animations loaded as an image containing each frame stacked vertically
jumpscare_sheet_right = pygame.image.load("assets/freddy_jumpsheet.jpg")
jumpscare_sheet_left = pygame.image.load("assets/bonnie_jumpsheet.jpg")
jumpscare_sheet_power = pygame.image.load("assets/no_power_jumpsheet.jpg")
jumpscare_sheet_right_frames = 28
jumpscare_sheet_left_frames = 11
jumpscare_sheet_power_frames = 21

# Load image for the background
background = pygame.image.load("assets/office.png")

# Load images for the doors
left_animatronic_image = pygame.image.load("assets/bonnie.png")
left_door_image = pygame.image.load("assets/doorleft.png")
right_animatronic_image = pygame.image.load("assets/freddy.png")
right_door_image = pygame.image.load("assets/doorright.png")

# Positions of doors and animatronic sprites
left_door_pos = pygame.Vector2(58, 59)
left_animatronic_pos = pygame.Vector2(56, 89)
left_button_bounds = pygame.rect.Rect(6, 163, 40, 110)
right_door_pos = pygame.Vector2(545, 59)
right_animatronic_pos = pygame.Vector2(555, 89)
right_button_bounds = pygame.rect.Rect(623, 163, 40, 110)

# Timer variable that stores how long the door will remain closed for
left_door_close = 1.0
right_door_close = 1.0

# The length of time that the door stays closed
door_close_length: float = 3.0

# The range of times that the animatronics can take to arrive at each door
animatronic_max_distance = 60
animatronic_min_distance = 40

default_background_rect = screen.screen_rect

# The amount of pixels on the border of the background along the y axis
background_padding_y = int((background.get_height() - screen.screen_rect.height) / 2)

# The amount of pixels on the border of the background along the x axis
background_padding_x = int((background.get_width() - screen.screen_rect.width) / 2)

# Move the draw position back by the padding to make it have a border around the edges
default_background_rect.x -= background_padding_x
default_background_rect.y -= background_padding_y

# Amount of pixel the mouse has to move to pan the background by 1 pixel, negative values reverse direction of movement
background_pan = -20

left_animatronic_distance: float = 1.0
right_animatronic_distance: float = 1.0

# Amount of seconds given to notice the animatronic before you lose
animatronic_warning_time = 12

# Fade in slower for nightmare mode to make it more fair
nightmare_warning_time = 30

background_draw_offset = pygame.Vector2(0, 0)

caught: str = ""


# Helper function to constrain a value between a specified minimum and maximum
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


# Resets and initialises variables for a new game session
def new_game():
    global left_animatronic_distance
    global right_animatronic_distance
    global left_door_close
    global right_door_close
    global caught

    # Reset game state flags and door timers
    caught = ""
    left_door_close = 0
    right_door_close = 0

    # Randomise the starting distance of the animatronics
    left_animatronic_distance = random.randrange(
        animatronic_min_distance, animatronic_max_distance
    )
    right_animatronic_distance = random.randrange(
        animatronic_min_distance, animatronic_max_distance
    )


# Handles the 2.5D parallax effect for the background based on mouse position
def draw_game_background():
    global background_draw_offset

    # Calculate how far the mouse is from the center of the game window
    mouse_offset_from_center_x = (
        screen.pygame.mouse.get_pos()[0] - screen.screen_rect.width / 2
    )
    mouse_offset_from_center_y = (
        screen.pygame.mouse.get_pos()[1] - screen.screen_rect.height / 2
    )

    # Convert to integer because drawing rectangles only use full pixels and store their values as int
    # Divide by background_pan to scale down the movement (creates the parallax effect)
    offset_bg_x = int(mouse_offset_from_center_x / background_pan)
    offset_bg_y = int(mouse_offset_from_center_y / background_pan)

    # Clamp the panning values so the player cannot see past the edges of the background image
    offset_bg_x = clamp(offset_bg_x, -background_padding_x, background_padding_x)
    offset_bg_y = clamp(offset_bg_y, -background_padding_y, background_padding_y)

    # Apply the offset to the default centered background position
    background_draw_offset.x = offset_bg_x + default_background_rect.x
    background_draw_offset.y = offset_bg_y + default_background_rect.y

    # Render the background image to the calculated position
    screen.screen.blit(background, background_draw_offset)


# Updates the game logic, countdowns, and enemy distances every frame
def update(delta: float):
    global left_animatronic_distance
    global right_animatronic_distance
    global left_door_close
    global right_door_close
    global caught

    # Animatronics only move closer if their respective doors are not currently closed
    if left_door_close <= 0:
        left_animatronic_distance -= delta
    if right_door_close <= 0:
        right_animatronic_distance -= delta

    # Always count down the remaining time the doors stay shut
    left_door_close -= delta
    right_door_close -= delta

    # If an animatronic reaches a distance below 0, the player is caught
    if left_animatronic_distance < 0:
        caught = "left"
    if right_animatronic_distance < 0:
        caught = "right"


# Closes the left door to defend against the left animatronic
def close_door_left():
    global left_door_close
    global left_animatronic_distance

    # Do nothing if the door is already closed
    if left_door_close > 0:
        return

    # Penalise the player's survival time for actively using the door
    globals.survival_time += globals.door_time_penalty
    door_sound.play()

    # Lock the door and push the animatronic back to a new random distance
    left_door_close = door_close_length
    left_animatronic_distance = random.randrange(
        animatronic_min_distance, animatronic_max_distance
    )


# Closes the right door to defend against the right animatronic
def close_door_right():
    global right_door_close
    global right_animatronic_distance

    # Do nothing if the door is already closed
    if right_door_close > 0:
        return

    # Penalise the player's survival time for actively using the door
    globals.survival_time += globals.door_time_penalty
    door_sound.play()

    # Lock the door and push the animatronic back to a new random distance
    right_door_close = door_close_length
    right_animatronic_distance = random.randrange(
        animatronic_min_distance, animatronic_max_distance
    )


# Checks if the user clicked on either of the physical door buttons in the game world
def click():
    mouse_position = pygame.mouse.get_pos()

    # Compensate for the parallax background draw offset to check collisions accurately
    if left_button_bounds.collidepoint(mouse_position - background_draw_offset):
        close_door_left()
    if right_button_bounds.collidepoint(mouse_position - background_draw_offset):
        close_door_right()


# Renders the doors or the approaching animatronics depending on the current game state
def draw_animatronics():
    # Adjust the reaction/warning window depending on the selected game difficulty
    warning_time = animatronic_warning_time
    if globals.difficulty == "Nightmare":
        warning_time = nightmare_warning_time

    # Process the left side visuals
    if left_door_close > 0:
        screen.screen.blit(left_door_image, left_door_pos + background_draw_offset)
    elif left_animatronic_distance < warning_time:
        # Fade the animatronic in (increase alpha) the closer it gets to 0
        alpha = 255 - int((left_animatronic_distance / warning_time) * 255)
        left_animatronic_image.set_alpha(alpha)
        screen.screen.blit(
            left_animatronic_image, left_animatronic_pos + background_draw_offset
        )

    # Process the right side visuals
    if right_door_close > 0:
        screen.screen.blit(right_door_image, right_door_pos + background_draw_offset)
    elif right_animatronic_distance < warning_time:
        # Fade the animatronic in (increase alpha) the closer it gets to 0
        alpha = 255 - int((right_animatronic_distance / warning_time) * 255)
        right_animatronic_image.set_alpha(alpha)
        screen.screen.blit(
            right_animatronic_image, right_animatronic_pos + background_draw_offset
        )


# Draws a black mask tied to the mouse to simulate a flashlight in nightmare mode
def draw_flashlight():
    mouse_position = pygame.mouse.get_pos()

    # Calculate draw position to keep the bright spot centered exactly on the cursor
    draw_position = (
        mouse_position[0] - screen.window_size[0],
        mouse_position[1] - screen.window_size[1],
    )

    screen.screen.blit(flashlight_image, draw_position)


# Plays the jumpscare animation sequence
def jumpscare(left=False, power=True):
    # Stop music and play the jumpscare sound
    pygame.mixer_music.stop()
    jumpscare_sound.play()

    # Determine which sprite sheet to use and how many frames it has
    frame_count = jumpscare_sheet_right_frames
    if left:
        frame_count = jumpscare_sheet_left_frames
    if not power:
        frame_count = jumpscare_sheet_power_frames

    # Loop through the vertical sprite sheet to draw the animation frame-by-frame
    for i in range(frame_count):
        if not power:
            screen.screen.blit(jumpscare_sheet_power, (0, i * -360))
        elif left:
            screen.screen.blit(jumpscare_sheet_left, (0, i * -360))
        else:
            screen.screen.blit(jumpscare_sheet_right, (0, i * -360))

        pygame.display.flip()  # Update the display
        screen.clock.tick(15)  # Limits FPS to 15 to match animation source framerate

    # Cut off jumpscare sound once the animation is completed to stop it carrying into next screen
    jumpscare_sound.stop()
