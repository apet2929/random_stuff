import math

import pygame
from ui import Page, Text, Font


class NewText(Text):
    def __init__(self, text, screen_size, center_pos, width: int, f: Font, color):
        self.font = f
        self.width = width
        (self._chars_per_line, self._char_size) = self._calc_wrap_vals()
        super().__init__(text, screen_size, center_pos, f, color)

    def create_surface(self):
        lines = self.split_text_into_lines(self.text)
        image = pygame.Surface((self.width, len(lines) * self._char_size[1]))
        image.fill((255, 0, 255))
        image.set_colorkey((255, 0, 255, 255), pygame.RLEACCEL)
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, self.color, (255, 0, 255))
            image.blit(surf, (0, i * self._char_size[1]))
        return image

    def split_text_into_lines(self, text: str):
        lines = []
        current_line = text
        while len(current_line) > self._chars_per_line:
            end_of_line = self.last_fitting_word_in_line_index(current_line)
            lines.append(current_line[0: end_of_line])
            current_line = current_line[end_of_line:]
        lines.append(current_line)
        return lines

    def last_fitting_word_in_line_index(self, line):
        char_counter = 0
        for i, word in enumerate(line.split()):
            char_counter += len(word)
            if char_counter >= self._chars_per_line:
                return char_counter - len(word)  # return the index of the start of the 1st word that won't fit in line
            char_counter += 1
        return -1  # return the end of the string if all words fit

    def _calc_wrap_vals(self):
        surf = self.font.render("Ao", False, (0, 0, 0))
        char_width = math.ceil(surf.get_width() / 2)
        char_height = math.ceil(surf.get_height() * 1.1)
        chars_per_line = math.ceil((self.width / char_width) * 0.9)
        return chars_per_line, (char_width, char_height)


class TestPage(Page):
    def __init__(self):
        test_text = NewText("This is a test ye This is a test This is a test This is a test This is a test",
                            (WIDTH, HEIGHT), (50, 50), WIDTH//2, f, (0, 0, 0))
        super().__init__([], [test_text])


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    WIDTH = 640
    HEIGHT = 480
    f = Font(20, WIDTH, False, False)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    page = TestPage()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                pygame.display.update()
                size = pygame.display.get_surface().get_size()
                page.resize((WIDTH, HEIGHT), size)
                WIDTH, HEIGHT = size

        screen.fill((255, 255, 255))
        page.handle_input(events)
        page.update()
        page.render(screen)
        pygame.display.flip()

    pygame.quit()
