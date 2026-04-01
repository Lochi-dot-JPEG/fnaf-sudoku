import pygame

# Initialises pygame across the whole project, needed to import fonts
pygame.init()

# RGB tuples defining the visual palette of the Sudoku board and text
defaultFontColor = (153, 185, 207)
locked_tile_colour = (76, 83, 95)
default_tile_colour = (42, 49, 54)
selected_tile_colour = (170, 202, 224)
board_background_color = (153, 185, 207)
error_tile_color = (140, 40, 57)

# Alpha transparency value for the player's active grid selection
selected_tile_alpha = 120

# Stores current difficulty setting (e.g., "Normal", "Nightmare")
difficulty: str = "Normal"
# Defines active player count for session
player_count: int = 1

# Survival & Time Mechanics
# Tracks the total time in milliseconds elapsed during the active round
survival_time: int = 0
# Maximum survival limit representing 15 minutes of gameplay translated to milliseconds
max_time = 60 * 15 * 1000
# Penalty value applied in milliseconds whenever a player closes doors
door_time_penalty = 10 * 1000

# Text colour for the number inside Sudoku cells
tile_text_color = (170, 202, 224)
selected_tile_text_color = (255, 255, 255)

# Pre-loading project-wide custom TTF font files at designated sizes
tile_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 16)
button_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 20)
time_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 12)
tutorial_font = time_font
title_font = pygame.font.Font("assets/JetBrainsMonoNL-Bold.ttf", 32)

# Global flag used to break main loops and exit player to the title screen
returning_to_title: bool = False

# Absolute paths pointing to the background ambience and failure sound effects
ambient_music_path = str("assets/loopingambience.ogg")
musicbox_music_path = str("assets/music_box.ogg")

tutorial_texts = [
    [
        "Low on money, you took this part time job working",
        "at Five Night's at Freddy's Pizzeria.",
        "That was until the lights outside your office went",
        "out, and a musicbox begun to chime.",
        "The exit locked, and a your computer lit up with a",
        "sudoku puzzle. ",
        "You must solve the sudoku puzzle quickly, to make",
        "your exit before your power runs out, while ",
        "making sure the animatronics do not catch you.",
        "",
        "This game is best experienced with volume on.",
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
        "Close doors uses power. Every time you close the",
        "door, you lose 20 seconds of power.",
        "",
        "If you leave them too long, you will get caught.",
    ],
    [
        "Each difficulty slightly changes how the game plays.",
        "",
        "Normal difficulty gives you simple puzzles.",
        "",
        "Hard difficulty gives you much harder puzzles.",
        "",
        "Nightmare difficulty restricts your vision",
        "and also gives you the same puzzles as hard mode.",
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
        "If multiple players complete the puzzle then",
        "whoever did it in the least amount of time will win.",
    ],
]
