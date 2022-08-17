import pygame

from text_wrap import NewText
from ui import Font
import pytest

def test_split_text_into_lines():
    pygame.font.init()
    text = NewText("This is a test This is a test This is a test This is a test This is a test", (100, 100), (50, 50), 100,
                   Font(12, 100, False, False), (0, 0, 0))
    lines = text.split_text_into_lines("This is a test This is a test This is a test This is a test This is a test")
    print(lines)


