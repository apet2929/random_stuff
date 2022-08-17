class Color:
    def __init__(self, rgb:tuple = None, hsv:tuple = None) -> None:
        if rgb:
            self.red = rgb[0]
            self.green = rgb[1]
            self.blue = rgb[2]
            hsv = Color.rgb_to_hsv(self.red, self.green, self.blue)
            self._hue = hsv[0]
            self._saturation = hsv[1]
            self._value = hsv[2]
        elif hsv:
            self._hue = hsv[0] % 360
            self._saturation = hsv[1]
            self._value = hsv[2]
            rgb = Color.hsv_to_rgb(self._hue, self._saturation, self._value)
            self.red = rgb[0]
            self.green = rgb[1]
            self.blue = rgb[2]

        self.rgb: tuple = self.get_rgb()
        self.hsv = (self._hue, self._saturation, self._value)

    """
    Takes a tuple of 3 ColorParts
    """
    def set_rgb(self, rgb):
        self.rgb = rgb
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def get_rgb(self):
        return (self.red, self.green, self.blue)

    def get_hsv(self):
        return (self._hue, self._saturation, self._value)

    def rgb_to_hsv(red: float, green: float, blue: float) -> tuple:
        rp = red/ 255.0
        gp = green / 255.0
        bp = blue / 255.0

        cMax = max(rp, gp, bp)
        cMin = min(rp, gp, bp)
        
        delta = cMax - cMin

        hue = 0
        if delta == 0:
            hue = 0
        elif cMax == rp:
            temp = (gp - bp) / delta
            hue = 60 * (temp%6) 
        elif cMax == gp:
            temp = (bp - rp) / delta
            hue = 60 * (temp+2) 
        elif cMax == bp:
            temp = (rp - gp) / delta
            hue = 60 * (temp+4)

        saturation = 0
        if cMax != 0:
            saturation = delta / cMax

        value = cMax

        return (hue, saturation, value)
    
    def hsv_to_rgb(hue, saturation, value) -> tuple:

        c = value * saturation
        x = c * (1 - abs(((hue / 60) % 2) - 1))
        m = value - c

        rp = 0
        gp = 0
        bp = 0
        if hue >= 300:
            rp = c
            bp = x
        elif hue >= 240 and hue < 300:
            rp = x
            bp = c
        elif hue >= 180 and hue < 240:
            gp = x
            bp = c
        elif hue >= 120 and hue < 180:
            gp = c
            bp = x
        elif hue >= 60 and hue < 120:
            rp = x
            gp = c
        elif hue >= 0 and hue < 60:
            rp = c
            gp = x
        
        r = (rp + m) * 255
        g = (gp + m) * 255
        b = (bp + m) * 255
        return (r, g, b)

    @property 
    def hue(self) -> float:
        return self._hue
    
    #TODO: Turn HSV and RGB into properties
    @hue.setter
    def hue(self, h):
        h = h % 360
        self._hue = h

        red, green, blue = Color.hsv_to_rgb(self._hue, self.saturation, self.value)
        self.red = red
        self.green = green
        self.blue = blue
        self.rgb = self.get_rgb()

    @property
    def saturation(self) -> float:
        return self._saturation
    
    @saturation.setter
    def saturation(self, sat):
        if sat > 1:
            sat = sat % 1
        self._saturation = sat
        red, green, blue = Color.hsv_to_rgb(self.hue, sat, self.value)
        self.red = red
        self.green = green
        self.blue = blue
        self.rgb = self.get_rgb()

    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, val):
        if val > 1:
            val = val % 1
        self._value = val
        red, green, blue = Color.hsv_to_rgb(self.hue, self.saturation, val)
        self.red = red
        self.green = green
        self.blue = blue
        self.rgb = self.get_rgb()
        

    def add_rgb(self, rVal, gVal, bVal):
        self.red += rVal
        self.green += gVal
        self.blue += bVal
        hsv = Color.rgb_to_hsv(self.red, self.green, self.blue)
        self._hue = hsv[0]
        self._saturation = hsv[1]
        self._value = hsv[2]
        
    
    def add_hsv(self, hue, sat, val):
        self.hue += hue
        self.saturation += sat
        self.value += val
    
        self.set_rgb(Color.hsv_to_rgb(self.hue, self.saturation, self.value))
    
    def __str__(self):
        return f"rgb = ({self.red}, {self.green}, {self.blue}) hsv = ({int(self.hue)}*, {int(self.saturation*100)}%, {int(self.value*100)}%)"
