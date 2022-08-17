from enum import Enum

class Fonts:
    # Static class that holds a list of fonts
    # Don't initialize

    _fonts = []
    class FontType(Enum):
        SMALL_FONT = 0
        LARGE_FONT = 1
        DEFAULT_FONT = 2

    def init_font(font, type: FontType):
        Fonts._fonts[type] = font
    def get(type: FontType):
        if type in range(len(Fonts._fonts)):
            return Fonts._fonts[type]
        else:
            print(f"Font {type} not initialized!")
    def resize(self, scaleX, scaleY):
        for font in self._fonts:
            font.resize(scaleX, scaleY) # defined in font class

"""
Usage

title_text.font = FontType.LARGE_FONT

(in Text.render)
text_surface = Fonts.get(this.font).render(text)
"""
