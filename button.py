import pygame
import globals


# Button class that extends the pygame.sprite.Sprite class for visible game objects
# Used for the title screen and ask menu

button_height = 32
# Returns label text when pressed
class Button():
    # Text shown on the button
    text : str = ""
    pressed : bool = False
    # Surface that the button text is rendered to
    text_surface : pygame.Surface
    text_offset = pygame.Vector2(8,2)

    # Surface that the button outline is rendered to
    outline_surface : pygame.Surface
    outline_position : pygame.Vector2

    mouse_rect : pygame.rect.Rect


    # Function run when the button is initially created using Button()
    def __init__(self, position, label, font_colour = globals.defaultFontColor, width = 200):
        # Sets text variable to the inputted label variable
        self.text = label
        self.text_surface = globals.button_font.render(label, True, font_colour)

        rect = pygame.rect.Rect(0,0, max(width,self.text_surface.get_width() + 16),button_height)
        self.mouse_rect = pygame.rect.Rect(position.x,position.y, width,button_height)
        self.outline_surface = pygame.surface.Surface((rect.width,rect.height));

        pygame.draw.rect(self.outline_surface, font_colour, rect, 2)
        self.outline_position = position


    def update_hover(self):
        mouse_position = pygame.mouse.get_pos()
        if self.mouse_rect.collidepoint(mouse_position[0], mouse_position[1]):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True


    def draw(self, surface : pygame.Surface):
        mouse_position = pygame.mouse.get_pos()
        if self.mouse_rect.collidepoint(mouse_position[0], mouse_position[1]):
            surface.blit(self.outline_surface, self.outline_position)
        surface.blit(self.text_surface, self.outline_position + self.text_offset)

