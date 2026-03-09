from os import timerfd_create
from time import sleep
from turtle import pos
import pygame



# TODO store all colours, fonts and stuff globally in an import
defaultFontColor = (255, 255, 255)
button_font = pygame.font.Font('assets/JetBrainsMonoNL-Bold.ttf', 20)

# Button class that extends the pygame.sprite.Sprite class for visible game objects
# Used for the title screen and ask menu
# Returns label text when pressed
class Button():
    # Text shown on the button
    text : str = ""

    pressed : bool = False
    # Surface that the button is rendered to
    text_surface : pygame.Surface
    text_offset = pygame.Vector2(8,2)

    outline_surface : pygame.Surface
    outline_position : pygame.Vector2

    mouse_rect : pygame.rect.Rect

    # Font colour stored as a tuple of three integers
    #font_colour : tuple[int,int,int]

    # Function run when the button is initially created using Button()
    def __init__(self, position : pygame.Vector2, label : str, font_colour = defaultFontColor, width : int = 200):
        # Sets text variable to the inputted label variable
        self.text = label

        self.text_surface = button_font.render(label, True, font_colour)

        height = 32

        rect = pygame.rect.Rect(0,0, width,height)
        self.mouse_rect = pygame.rect.Rect(position.x,position.y, width,height)
        self.outline_surface = pygame.surface.Surface((width,height));

        pygame.draw.rect(self.outline_surface, font_colour, rect, 2)

        self.outline_position = position

    def draw(self, surface : pygame.Surface):
        # TODO make this only happen when hovered

        mouse_position = pygame.mouse.get_pos()
        if self.mouse_rect.collidepoint(mouse_position[0], mouse_position[1]):
            surface.blit(self.outline_surface, self.outline_position)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                #waiting = True
                #while waiting:
                    #print("sleeps")
                    #waiting = pygame.mouse.get_pressed()[0]
        surface.blit(self.text_surface, self.outline_position + self.text_offset)

