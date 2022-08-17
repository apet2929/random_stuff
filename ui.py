from pygame import Rect, Surface, draw, font, SRCALPHA
import pygame
from pygame.transform import scale
import os.path


class Page:
    def __init__(self, buttons, texts, input_box: bool = False) -> None:
        self.buttons: list[Button] = buttons
        self.texts: list[Text] = texts

    def render(self, screen: Surface):

        for button in self.buttons:
            button.draw(screen)

        for text in self.texts:
            text.draw(screen)

    def handle_input(self, events):
        # Convenient hook to override
        pass

    def update(self):
        # Convenient hook to override
        pass

    def resize(self, old_screen_size, new_screen_size):
        print("Resizing")
        for button in self.buttons:
            button.resize(old_screen_size, new_screen_size)
        for text in self.texts:
            text.resize(old_screen_size, new_screen_size)

    """
    Returns the index of the button clicked or None if none were clicked
    """

    def on_click(self, mouse_pos) -> int or None:
        for i in range(len(self.buttons)):
            if self.buttons[i].check_click(mouse_pos):
                return i
        return None


class Button:
    """
    text: string of text to be drawn on the button
    screen_size: width and height of screen
    pos: tuple, x and y are floats from 0 to 100, position relative to the screen width and height
    size: tuple, floats from 0 to 100, width and height relative to screen w/h
    rect_color1: rgba of first color in button gradient
    rect_color2: rgba of second color in button gradient
    text_color: rgba of the text color
    font: the font to be used when drawing the text
    """

    def __init__(self, text: str, screen_size: tuple, center_pos: tuple, size: tuple, rect_color1: tuple,
                 rect_color2: tuple, text_color: tuple, font: font.Font, rad: float = 45) -> None:
        self.rect = Button.get_rect(screen_size, center_pos[0] - size[0] / 2, center_pos[1] - size[1] / 2, size[0],
                                    size[1])
        self.text = text
        self.font = font
        self.rad = rad
        self.colors = [rect_color1, rect_color2, text_color]
        self.image = Surface((self.rect.width, self.rect.height), SRCALPHA)
        self.create_surface()

    def get_rect(screen_size, percentX, percentY, percentW, percentH) -> Rect:
        x, y = percent_to_pixels((percentX, percentY), screen_size)
        w, h = percent_to_pixels((percentW, percentH), screen_size)
        return Rect(x, y, w, h)

    """
    Sets self.image to the button w/ gradient and text
    """

    def create_surface(self):
        # Draw button w/ gradient
        y = 0
        width = self.rect.width
        height = self.rect.height
        c1 = [self.colors[0][0], self.colors[0][1], self.colors[0][2]]
        c2 = [self.colors[1][0], self.colors[1][1], self.colors[1][2]]
        c3 = []
        for i in range(int(height - self.rad)):
            c1[0] += (c2[0] - c1[0]) / (height - self.rad)
            c1[1] += (c2[1] - c1[1]) / (height - self.rad)
            c1[2] += (c2[2] - c1[2]) / (height - self.rad)
            c3 = (c1[0], c1[1], c1[2])
            draw.rect(self.image, c3, Rect(0, y, width, self.rad), int(self.rad / 2), self.rad)
            y += 1

        # Draw text
        text_surface = self.font.render(self.text, True, self.colors[2])
        textRect = text_surface.get_rect()
        textRect.center = self.image.get_rect().center

        self.image.blit(text_surface, textRect)

    """
    old_screen_size: tuple, old width and height of screen
    """

    def resize(self, old_screen_size, new_screen_size):
        percentX, percentY = pixels_to_percent((self.rect.x, self.rect.y), old_screen_size)
        percentW, percentH = pixels_to_percent((self.rect.w, self.rect.h), old_screen_size)
        self.rect = Button.get_rect(new_screen_size, percentX, percentY, percentW, percentH)
        self.image = Surface((self.rect.width, self.rect.height), SRCALPHA)
        self.create_surface()

    def set_color(self, rect_color1=None, rect_color2=None, text_color=None):
        if not rect_color1:
            rect_color1 = self.colors[0]
        if not rect_color2:
            rect_color2 = self.colors[1]
        if not text_color:
            text_color = self.colors[2]

        self.colors = [rect_color1, rect_color2, text_color]
        self.create_surface()

    def set_text(self, text: str):
        self.text = text
        self.create_surface()

    """
    pos: tuple, percentage x and y of screen size
    """

    def set_pos(self, pos, screen_size):
        x, y = percent_to_pixels(pos, screen_size)
        self.rect.x = x
        self.rect.y = y

    def set_center(self, pos, screen_size):
        x, y = percent_to_pixels(pos, screen_size)
        self.rect.center = (x, y)

    """
    mouse_pos: tuple of mouse x and y
    returns True if mouse pos is within bounds of the button
    """

    def check_click(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos) == 1

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)


class Font:
    def __init__(self, font_size, screen_width, bold, italic) -> None:
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.value = font.Font(os.path.join("assets", "font.ttf"), int(screen_width / self.font_size), bold=self.bold,
                               italic=self.italic)

    def resize(self, screen_width):
        self.value = font.Font(os.path.join("assets", "font.ttf"), int(screen_width / self.font_size), bold=self.bold,
                               italic=self.italic)

    def render(self, text, antialias, color, background=None):
        return self.value.render(text, antialias, color, background)


class Text:
    def __init__(self, text, screen_size, center_pos, f: Font, color) -> None:
        self.text = text
        self.font = f
        self.color = color
        self.center_percent = center_pos
        self.image = self.create_surface()

        # Creates a copy to avoid moving the actual image
        self.rect = self.image.get_rect().copy()
        center = percent_to_pixels(center_pos, screen_size)
        self.rect.center = center

    def set_topleft(self, top=None, left=None):
        r = self.image.get_rect()

        if top:
            r.top = top
        if left:
            r.left = left

    def set_rect(self, rect):
        self.rect = rect

    def create_surface(self):
        return self.font.render(self.text, True, self.color)

    def set_text(self, text):
        self.text = text
        center = self.rect.center
        self.image = self.create_surface()
        self.rect = self.image.get_rect(center=center)

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def resize(self, new_screen_size):
        self.font.resize(new_screen_size[0])
        self.image = self.create_surface()
        self.rect = self.image.get_rect().copy()
        self.rect.center = percent_to_pixels(self.center_percent, new_screen_size)


class InputBox:
    def __init__(self, screen_size, pos: tuple, size: tuple, f: font.Font, color_inactive: tuple, color_active: tuple,
                 default_text=''):
        x, y = percent_to_pixels(pos, screen_size)
        w, h = percent_to_pixels(size, screen_size)
        self.rect = pygame.Rect(x, y, w, h)
        self.font: font.Font = f
        self.active = 0
        self.colors = (color_inactive, color_active)
        self.text = default_text
        self.txt_surface = f.render(default_text, True, self.color)
        self.min_width = screen_size[0] * size[0]

    @property
    def color(self):
        return self.colors[self.active]

    def toggle_active(self):
        if self.active == 0:
            self.active = 1
        elif self.active == 1:
            self.active = 0

    def isActive(self):
        return self.active == 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.toggle_active()
            else:
                self.active = 0
            # Change the current color of the input box.
        if event.type == pygame.KEYDOWN:
            if self.isActive:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.min_width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        draw.rect(screen, self.color, self.rect, 2)


"""
Copyright 2021, Silas Gyger, silasgyger@gmail.com, All rights reserved.
Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""


class TextInputManager:
    """
    Keeps track of text inputted, cursor position, etc.
    Pass a validator function returning if a string is valid,
    and the string will only be updated if the validator function
    returns true.
    For example, limit input to 5 characters:
    ```
    limit_5 = lambda x: len(x) <= 5
    manager = TextInputManager(validator=limit_5)
    ```

    :param initial: The initial string
    :param validator: A function string -> bool defining valid input
    """

    def __init__(self,
                 initial="",
                 validator=lambda x: True):

        self.left = initial  # string to the left of the cursor
        self.right = ""  # string to the right of the cursor
        self.validator = validator

    @property
    def value(self):
        """ Get / set the value currently inputted. Doesn't change cursor position if possible."""
        return self.left + self.right

    @value.setter
    def value(self, value):
        cursor_pos = self.cursor_pos
        self.left = value[:cursor_pos]
        self.right = value[cursor_pos:]

    @property
    def cursor_pos(self):
        """ Get / set the position of the cursor. Will clamp to [0, length of input]. """
        return len(self.left)

    @cursor_pos.setter
    def cursor_pos(self, value):
        complete = self.value
        self.left = complete[:value]
        self.right = complete[value:]

    def update(self, events):
        """
        Update the interal state with fresh pygame events.
        Call this every frame with all events returned by `pygame.event.get()`.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                v_before = self.value
                c_before = self.cursor_pos
                self._process_keydown(event)
                if not self.validator(self.value):
                    self.value = v_before
                    self.cursor_pos = c_before

    def _process_keydown(self, ev):
        attrname = f"_process_{pygame.key.name(ev.key)}"
        if hasattr(self, attrname):
            getattr(self, attrname)()
        else:
            self._process_other(ev)

    def _process_delete(self):
        self.right = self.right[1:]

    def _process_backspace(self):
        self.left = self.left[:-1]

    def _process_right(self):
        self.cursor_pos += 1

    def _process_left(self):
        self.cursor_pos -= 1

    def _process_end(self):
        self.cursor_pos = len(self.value)

    def _process_home(self):
        self.cursor_pos = 0

    def _process_return(self):
        pass

    def _process_other(self, event):
        self.left += event.unicode


class TextInputVisualizer:
    """
    Utility class to quickly visualize textual input, like a message or username.
    Pass events every frame to the `.update` method, then get the surface
    of the rendered font using the `.surface` attribute.
    All arguments of constructor can also be set via attributes, so e.g.
    to change `font_color` do
    ```
    inputVisualizer.font_color = (255, 100, 0)
    ```
    The surface itself is lazily re-rendered only when the `.surface` field is 
    accessed, and if any parameters changed since the last `.surface` access, so
    values can freely be changed between renders without performance overhead.
    :param manager: The TextInputManager used to manage the user input
    :param font_object: a pygame.font.Font object used for rendering
    :param antialias: whether to render the font antialiased or not
    :param font_color: color of font rendered
    :param cursor_blink_interal: the interval of the cursor blinking, in ms
    :param cursor_width: The width of the cursor, in pixels
    :param cursor_color: The color of the cursor
    """

    def __init__(self,
                 manager=None,
                 font_object=None,
                 antialias=True,
                 font_color=(0, 0, 0),
                 cursor_blink_interval=300,
                 cursor_width=3,
                 cursor_color=(0, 0, 0)
                 ):

        self._manager = TextInputManager() if manager is None else manager
        self._font_object = pygame.font.Font(pygame.font.get_default_font(), 25) if font_object is None else font_object
        self._antialias = antialias
        self._font_color = font_color

        self._clock = pygame.time.Clock()
        self._cursor_blink_interval = cursor_blink_interval
        self._cursor_visible = False
        self._last_blink_toggle = 0

        self._cursor_width = cursor_width
        self._cursor_color = cursor_color

        self._surface = pygame.Surface((self._cursor_width, self._font_object.get_height()))
        self._rerender_required = True

    @property
    def value(self):
        """ Get / set the value of text alreay inputted. Doesn't change cursor position if possible."""
        return self.manager.value

    @value.setter
    def value(self, v):
        self.manager.value = v

    @property
    def manager(self):
        """ Get / set the underlying `TextInputManager` for this instance"""
        return self._manager

    @manager.setter
    def manager(self, v):
        self._manager = v

    @property
    def surface(self):
        """ Get the surface with the rendered user input """
        if self._rerender_required:
            self._rerender()
            self._rerender_required = False
        return self._surface

    @property
    def antialias(self):
        """ Get / set antialias of the render """
        return self._antialias

    @antialias.setter
    def antialias(self, v):
        self._antialias = v
        self._require_rerender()

    @property
    def font_color(self):
        """ Get / set color of rendered font """
        return self._font_color

    @font_color.setter
    def font_color(self, v):
        self._font_color = v
        self._require_rerender()

    @property
    def font_object(self):
        """ Get / set the font object used to render the text """
        return self._font_object

    @font_object.setter
    def font_object(self, v):
        self._font_object = v
        self._require_rerender()

    @property
    def cursor_visible(self):
        """ Get / set cursor visibility (flips again after `.cursor_interval` if continuously update)"""
        return self._cursor_visible

    @cursor_visible.setter
    def cursor_visible(self, v):
        self._cursor_visible = v
        self._last_blink_toggle = 0
        self._require_rerender()

    @property
    def cursor_width(self):
        """ Get / set width in pixels of the cursor """
        return self._cursor_width

    @cursor_width.setter
    def cursor_width(self, v):
        self._cursor_width = v
        self._require_rerender()

    @property
    def cursor_color(self):
        """ Get / set the color of the cursor """
        return self._cursor_color

    @cursor_color.setter
    def cursor_color(self, v):
        self._cursor_color = v
        self._require_rerender()

    @property
    def cursor_blink_interval(self):
        """ Get / set the interval of time with which the cursor blinks (toggles), in ms"""
        return self._cursor_blink_interval

    @cursor_blink_interval.setter
    def cursor_blink_interval(self, v):
        self._cursor_blink_interval = v

    def update(self, events: pygame.event.Event):
        """
        Update internal state.
        
        Call this once every frame with all events returned by `pygame.event.get()`
        """

        # Update self.manager internal state, rerender if value changes
        value_before = self.manager.value
        self.manager.update(events)
        if self.manager.value != value_before:
            self._require_rerender()

        # Update cursor visibility after self._blink_interval milliseconds
        self._clock.tick()
        self._last_blink_toggle += self._clock.get_time()
        if self._last_blink_toggle > self._cursor_blink_interval:
            self._last_blink_toggle %= self._cursor_blink_interval
            self._cursor_visible = not self._cursor_visible

            self._require_rerender()

        # Make cursor visible when something is pressed
        if [event for event in events if event.type == pygame.KEYDOWN]:
            self._last_blink_toggle = 0
            self._cursor_visible = True
            self._require_rerender()

    def _require_rerender(self):
        """
        Trigger a re-render of the surface the next time the surface is accessed.
        """
        self._rerender_required = True

    def _rerender(self):
        """ Rerender self._surface."""
        # Final surface is slightly larger than font_render itself, to accomodate for cursor
        rendered_surface = self.font_object.render(self.manager.value + " ",
                                                   self.antialias,
                                                   self.font_color)
        w, h = rendered_surface.get_size()
        self._surface = pygame.Surface((w + self._cursor_width, h))
        self._surface = self._surface.convert_alpha(rendered_surface)
        self._surface.fill((0, 0, 0, 0))
        self._surface.blit(rendered_surface, (0, 0))

        if self._cursor_visible:
            str_left_of_cursor = self.manager.value[:self.manager.cursor_pos]
            cursor_y = self.font_object.size(str_left_of_cursor)[0]
            cursor_rect = pygame.Rect(cursor_y, 0, self._cursor_width, self.font_object.get_height())
            self._surface.fill(self._cursor_color, cursor_rect)


def percent_to_pixels(percent, screen_size):
    x = int((percent[0] / 100) * screen_size[0])
    y = int((percent[1] / 100) * screen_size[1])
    return (x, y)


def pixels_to_percent(pos, screen_size):
    x = (pos[0] * 100) / screen_size[0]
    y = (pos[1] * 100) / screen_size[1]
    return (x, y)


def get_font(screen_width, size=11, bold=False, italic=False, underline=False) -> Font:
    f = Font(size, screen_width, bold, italic)
    return f


col1 = (43, 45, 66)
col2 = (141, 153, 174)
col3 = (237, 242, 244)
col4 = (239, 35, 60)
col5 = (217, 4, 41)

grad1 = col5
grad2 = col3
bgCol = col3
txtCol = col1
button1 = col2
button2 = col1
buttontxt = col3
