import pygame


defaultFontColor = (255, 255, 255)
button_font = pygame.font.Font('assets/JetBrainsMonoNL-Bold.ttf', 24)

# Button class that extends the pygame.sprite.Sprite class for visible game objects
# Used for the title screen and ask menu
# Returns label text when pressed
class Button():
    # Text shown on the button
    text : str = ""

    # Surface that the button is rendered to
    surface : pygame.Surface

    # Font colour stored as a tuple of three integers
    font_colour : tuple[int,int,int]

    # Function run when the button is initially created using Button()
    def __init__(self, position : pygame.Vector2, label : str, font_colour = defaultFontColor, width : int):
        # Sets text variable to the inputted label variable
        self.text = label

        # Creates a sprite, to store the rendered text
        pygame.sprite.Sprite.__init__(self)

        # Defaults to red font colour using font_red otherwise makes it white

        self.image = button_font.render(label, True, font_colour)

        # Makes the sprites rect the same as the rendered font image
        self.rect = self.image.get_rect()
        # Offsets the x position by the pos x value, removing the width of the buttons rect to center it
        # This is because it would originate the sprite from the top left corner so you have to account for that
        self.rect.x = int(position.x - self.rect.w / 2)
        # Offsets the y position by the pos y value
        self.rect.y = int(position.y)

    def draw(self, surface : pygame.Surface, position : pygame.Vector2):
        pass

