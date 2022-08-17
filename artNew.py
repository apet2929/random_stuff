import pygame
import math
from math import radians, sin, cos, pi
import pygame.draw, pygame.surface

pygame.init()

#tools:
# select
# line
# dotted
# square
# circle

# triangle?

screen = pygame.display.set_mode([1000,900])
state = 1
drawingSurface = pygame.Surface((1000, 700), pygame.SRCALPHA)
drawingSurface.fill((255,255,255))
strokes = []
selectedStrokes = []
redoStrokes = []
hasRedo = False
isDrawing = False
selectedStroke = None
currentStroke = None
colors = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255)]
index = 0
tool = 1
selectIndex = 0
sizeSlider = pygame.Rect(600, 830, 280, 26)
sizeCircle = pygame.Rect(630, 843, 35, 35)
circleIsDragging = False
currentColor = colors[index]
size = (sizeCircle.x-600)/8

hSlider = pygame.Rect(500,195, 35,35)
sSlider = pygame.Rect(500,255, 35,35)
vSlider = pygame.Rect(500,315, 35,35)
hSliding = False
sSliding = False
vSliding = False
wheelSurface = pygame.Surface((200,200), pygame.SRCALPHA)
xCoord = 0
yCoord = 0


def drawState():
	screen.fill((0,0,0))
	drawingSurface.fill((255,255,255))
	for stroke in strokes: #draws the stuff that you drew onto the screen
		stroke.drawStroke()
	if isDrawing and currentStroke != None: #draws the stroke youre currently making bc its not in the strokes array yet
		currentStroke.drawStroke()
	if selectedStroke != None: # draws a rectangle around the stroke you selected.
		pygame.draw.rect(drawingSurface, (0,255,0), selectedStroke.rect, 3)
	screen.blit(drawingSurface, (0,100)) #draws the shit u drew onto the screen
	for i in range(len(colors)): #draws top color menu
		if i == index:
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(49 + i*60, 21, 42, 42))
		else:
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(46 + i*60, 18, 48, 48))
		pygame.draw.rect(screen, colors[i], pygame.Rect(50 + i*60, 22, 40, 40))
	pygame.draw.rect(screen, (50, 10, 200), pygame.Rect(350, 17, 50, 50), border_radius=10) #button to open the color pick menu
	for i in range(5): #draws the tool picking menu
		if i == tool:
			pygame.draw.rect(screen, (100, 10, 110), pygame.Rect(30 + i*70, 820, 60,60), border_radius=20)
		else:
			pygame.draw.rect(screen, (150, 50, 180), pygame.Rect(30 + i*70, 820, 60,60), border_radius=20)
		if i == 4:
			pygame.draw.circle(screen, (30,0,50), (60 + i*70, 830), 20, 2)
	pygame.draw.rect(screen, (220,220,220), sizeSlider, border_radius=12)
	pygame.draw.circle(screen, (120,120,140), (sizeCircle.x, sizeCircle.y), sizeCircle.width/2)
	if selectedStroke != None:
		pygame.draw.rect(drawingSurface, (150,0,200), selectedStroke.rect, 5)

def drawUpdate():
	x, y = pygame.mouse.get_pos()
	if circleIsDragging and x in range(600, 880):
		sizeCircle.x = x
		if selectedStroke != None:
			selectedStroke.scale = (sizeCircle.x-600)/140
			selectedStroke.scalePos = sizeCircle.x
			selectedStroke.scaledSurface = pygame.transform.scale(selectedStroke.surface, (int(selectedStroke.surface.get_width()*selectedStroke.scale), int(selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion)))
			selectedStroke.rect.width, selectedStroke.rect.height = selectedStroke.surface.get_width()*selectedStroke.scale, selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion
	if isDrawing:
		if tool == 1 or tool == 2:
			currentStroke.points.append((x, y+100))
	if selectedStroke != None and selectedStroke.drag:
		pos = pygame.mouse.get_pos()
		selectedStroke.rect.x += pos[0]-selectedStroke.dragPoint[0]
		selectedStroke.rect.y += pos[1]-selectedStroke.dragPoint[1]
		selectedStroke.dragPoint = pos

def drawInput(events):
	global index, tool, size, circleIsDragging, isDrawing, currentStroke, selectIndex, selectedStroke, selectedStrokes, currentColor, strokes, state, redoStrokes, hasRedo
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			if not pygame.Rect(0,100,1000,700).collidepoint((x, y)): #clicked on tools/colors 
				for i in range(len(colors)): #colors
					if pygame.Rect(50 + i*60, 22, 40, 40).collidepoint((x,y)):
						index = i
						currentColor = colors[index]
				for i in range(5): #tools
					if pygame.Rect(30 + i*70, 820, 60,60).collidepoint((x,y)):
						tool = i
						selectIndex = 0
						selectedStrokes = []
						selectedStroke = None
						sizeCircle.x = size*8 + 600
				if sizeSlider.collidepoint((x,y)):
					sizeCircle.x = x
					if tool != 0:
						size = (sizeCircle.x-600)/8
					else:
						if selectedStroke != None:
							selectedStroke.scale = (sizeCircle.x-600)/140
							selectedStroke.scalePos = sizeCircle.x
							selectedStroke.scaledSurface = pygame.transform.scale(selectedStroke.surface, (int(selectedStroke.surface.get_width()*selectedStroke.scale), int(selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion)))
							selectedStroke.rect.width, selectedStroke.rect.height = selectedStroke.surface.get_width()*selectedStroke.scale, selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion
					circleIsDragging = True
				if pygame.Rect(350, 17, 50, 50).collidepoint((x,y)): #checks if u clicked on the open color picker menu button
					state = 2
			else: #clicked on drawing surface
				if tool != 0:
					isDrawing = True
					hasRedo = False
					if tool == 1 or tool == 2:
						currentStroke = Stroke(currentColor, size, tool)
						strokes.append(currentStroke)
					if tool == 3 or tool == 4:
						pos = pygame.mouse.get_pos()
						currentStroke = Shapes(currentColor, size, tool, (pos[0], pos[1]-100))
						strokes.append(currentStroke)
				elif tool == 0:
					selectedStrokes = []
					for stroke in strokes:
						if stroke.checkClick():
							selectedStrokes.append(stroke)
					if selectedStrokes != []:
						selectedStroke = selectedStrokes[selectIndex]
					pos = pygame.mouse.get_pos()
					if selectedStroke != None and selectedStroke.rect.collidepoint((pos[0], pos[1]-100)):
						selectedStroke.drag = True
						selectedStroke.dragPoint = pos
					if selectedStrokes != None and selectedStroke != None:
						sizeCircle.x = selectedStroke.scalePos
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if tool != 0:
					hasRedo = False
					isDrawing = True
					if tool == 1 or tool == 2:
						currentStroke = Stroke(currentColor, size, tool)
						strokes.append(currentStroke)
					if tool == 3 or tool == 4:
						pos = pygame.mouse.get_pos()
						currentStroke = Shapes(currentColor, size, tool, (pos[0], pos[1]-100))
						strokes.append(currentStroke)
			if event.key == pygame.K_LEFT:
				if tool == 0 and selectedStrokes != []:
					if selectIndex > 0:
						selectIndex -= 1
					else:
						selectIndex = len(selectedStrokes)-1
					if selectedStrokes != []:
						selectedStroke = selectedStrokes[selectIndex]
			if event.key == pygame.K_RIGHT:
				if tool == 0 and selectedStrokes != []:
					if selectIndex < len(selectedStrokes)-1:
						selectIndex += 1
					else:
						selectIndex = 0
					if selectedStrokes != []:
							selectedStroke = selectedStrokes[selectIndex]
			if event.key == pygame.K_DOWN:
				if tool == 0:
					if selectedStroke != None:
						if selectedStroke.scale > 0:
							selectedStroke.scale -= .02
							selectedStroke.scaledSurface = pygame.transform.scale(selectedStroke.surface, (int(selectedStroke.surface.get_width()*selectedStroke.scale), int(selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion)))
							selectedStroke.rect.width, selectedStroke.rect.height = selectedStroke.surface.get_width()*selectedStroke.scale, selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion
			if event.key == pygame.K_UP:
				if tool == 0:
					if selectedStroke != None:
						if selectedStroke.scale > 0:
							selectedStroke.scale += .02
							selectedStroke.scaledSurface = pygame.transform.scale(selectedStroke.surface, (int(selectedStroke.surface.get_width()*selectedStroke.scale), int(selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion)))
							selectedStroke.rect.width, selectedStroke.rect.height = selectedStroke.surface.get_width()*selectedStroke.scale, selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion
		if event.type == pygame.MOUSEBUTTONUP:
			circleIsDragging = False
			if tool != 0:
				size = (sizeCircle.x-600)/8
				if isDrawing:
					currentStroke.makeSurf()
					isDrawing = False
					currentStroke.finished = True
			else:
				if selectedStroke != None:
					selectedStroke.scale = (sizeCircle.x-600)/140
					selectedStroke.scalePos = sizeCircle.x
					selectedStroke.scaledSurface = pygame.transform.scale(selectedStroke.surface, (int(selectedStroke.surface.get_width()*selectedStroke.scale), int(selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion)))
					selectedStroke.rect.width, selectedStroke.rect.height = selectedStroke.surface.get_width()*selectedStroke.scale, selectedStroke.surface.get_width()*selectedStroke.scale*selectedStroke.proportion
			if tool == 0:
				if selectedStroke != None:
					selectedStroke.drag = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				if tool != 0:
					circleIsDragging = False
					if isDrawing:
						currentStroke.makeSurf()
						isDrawing = False
						currentStroke.finished = True
			if event.key == pygame.K_BACKSPACE:
				if len(strokes) > 0:
					if selectedStroke == None:
						redoStrokes.append(strokes[-1])
						hasRedo = True
						strokes = strokes[0:-1]
				if selectedStroke != None and selectedStrokes != None and len(selectedStrokes) > 0:
					redoStrokes.append(selectedStroke)
					hasRedo = True
					strokes.remove(selectedStroke)
					selectedStrokes.pop(selectIndex)
					if len(selectedStrokes) > 0:
						if selectIndex < len(selectedStrokes)-1:
							selectIndex += 1
						else:
							selectIndex = 0
						selectedStroke = selectedStrokes[selectIndex]
					else:
						selectedStrokes = None
						selectedStroke = None
			if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
				if hasRedo:
					strokes.append(redoStrokes[-1])
					redoStrokes = redoStrokes[:-1]
				if len(redoStrokes) < 1:
					hasRedo = False


def colorState():
    pygame.draw.rect(screen, (170,170,190), pygame.Rect(150,150, 700,600), border_radius=40)
    pygame.draw.rect(screen, (120,120,130), pygame.Rect(500,200, 280,25), border_radius=20)
    pygame.draw.rect(screen, (120,120,130), pygame.Rect(500,260, 280,25), border_radius=20)
    pygame.draw.rect(screen, (120,120,130), pygame.Rect(500,320, 280,25), border_radius=20)

    pygame.draw.circle(screen, (40,40,60), (hSlider.x + 10, hSlider.y + 17), 15)
    pygame.draw.circle(screen, (40,40,60), (sSlider.x + 10, sSlider.y + 17), 15)
    pygame.draw.circle(screen, (40,40,60), (vSlider.x + 10, vSlider.y + 17), 15)

    pygame.draw.circle(screen, (255,0,0), (xCoord, yCoord), 6)

    for i in range(5):
        pygame.draw.rect(screen, colors[i], pygame.Rect(190 + i*130, 500, 100,100), border_radius=30)
        if index == i:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(185 + i*130, 495, 110,110), 5, 35)
    
    pygame.draw.circle(wheelSurface, (0,0,0), (100,100), 100)
    wheelSurface.blit(wheel, (0,0))
    screen.blit(wheelSurface, (170,170))

def colorUpdate():
	global xCoord, yCoord
	if hSlider.x in range(500, 756) and hSliding:
		hSlider.x = pygame.mouse.get_pos()[0] - 10
	if hSlider.x > 755:
		hSlider.x = 755
	if hSlider.x < 500:
		hSlider.x = 500
	if sSlider.x in range(500, 756) and sSliding:
		sSlider.x = pygame.mouse.get_pos()[0] - 10
	if sSlider.x > 755:
		sSlider.x = 755
	if sSlider.x < 500:
		sSlider.x = 500
	if vSlider.x in range(500, 756) and vSliding:
		vSlider.x = pygame.mouse.get_pos()[0] - 10
	if vSlider.x > 755:
		vSlider.x = 755
	if vSlider.x < 500:
		vSlider.x = 500
		
	if hSliding or vSliding or sSliding:
		xCoord = sin((hSlider.x-500)/(255/360)*pi/180)*(sSlider.x-500)/285*100 + 270
		yCoord = cos((hSlider.x-500)/(255/360)*pi/180)*(sSlider.x-500)/285*100 + 270
	pygame.draw.circle(screen, (255,0,0), (xCoord, yCoord), 6)
	wheel.set_alpha(vSlider.x-500)

def colorInput(events):
	global hSliding, sSliding, vSliding, state, index, xCoord, yCoord, currentColor
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			x,y = pygame.mouse.get_pos()
			if hSlider.collidepoint(x,y):
				hSliding = True
			if sSlider.collidepoint(x,y):
				sSliding = True
			if vSlider.collidepoint(x,y):
				vSliding = True
			for i in range(5):
				if pygame.Rect(190 + i*130, 500, 100,100).collidepoint(x,y):
					index = i
					h, s, v = Color.rgb_to_hsv(colors[index][0], colors[index][1], colors[index][2])
					hSlider.x = h * 28/36 + 500
					sSlider.x = s*280 + 500
					vSlider.x = v*280 + 500
					xCoord = sin((hSlider.x-500)/(255/360)*pi/180)*(sSlider.x-500)/285*100 + 270
					yCoord = cos((hSlider.x-500)/(255/360)*pi/180)*(sSlider.x-500)/285*100 + 270
			if pygame.Rect(170,170, 200,200).collidepoint(x,y):
				dist = math.sqrt((x-270)**2 + (y-270)**2)
				if dist <= 100:
					col = wheelSurface.get_at((x-170,y-170))
					h, s, v = Color.rgb_to_hsv(col[0], col[1], col[2])
					hSlider.x = h * 28/36 + 500
					sSlider.x = s*280 + 500
					xCoord = x
					yCoord = y
					colors[index] = Color.hsv_to_rgb(h,s,v)
		if event.type == pygame.MOUSEBUTTONUP:
			hSliding = False
			sSliding = False
			vSliding = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				state = 1
				currentColor = colors[index]


def run(events):
    if state == 1:
        drawState()
        drawUpdate()
        drawInput(events)
    if state == 2:
        colorState()
        colorUpdate()
        colorInput(events)


class Stroke():
	def __init__(self, color, size, tool):
		self.points = []
		self.color = color
		self.size = int(size)
		self.rect = None
		self.surface = None
		self.finished = False
		self.scaledSurface = None
		self.proportion = 1 # ratio of top and side
		self.scale = 1 # amount to scale it by
		self.tool = tool
		self.drag = False
		self.dragPoint = (0,0)
		self.selected = False
		self.scalePos = 740
	
	def drawStroke(self):
		if self.finished:
			if self.scaledSurface != None:
				drawingSurface.blit(self.scaledSurface, (self.rect.x, self.rect.y))
			if self.selected:
				pygame.draw.rect(drawingSurface, (255,0,255), self.rect, 6)

		else:
			i = 0
			for point in self.points:
				if self.tool == 2:
					pygame.draw.circle(drawingSurface, self.color, (point[0], point[1]-200), self.size/2)
				elif self.tool == 1:
					if i < len(self.points)-1 and i > 1:
						pygame.draw.line(drawingSurface, self.color, (point[0], point[1]-200), (self.points[i+1][0], self.points[i+1][1]-200), self.size)
				i += 1

	def checkSinglePoint(self):
		if len(self.points) > 0:
			for i in range(len(self.points)-2):
				if not (self.points[i] == self.points[i+1]):
					return False
			return True
	
	def checkClick(self):
		x, y = pygame.mouse.get_pos()
		if self.rect.collidepoint(x, y-100):
			return True
		return False

	def makeSurf(self):
		if self.tool == 1 or self.tool == 2:
			if len(self.points) > 0:
				top = self.points[0][1]
				right = self.points[0][0]
				bottom = self.points[0][1]
				left = self.points[0][0]
				for i in range(len(self.points)):
					if self.points[i][1] < top:
						top = self.points[i][1]
					if self.points[i][0] < left:
						left = self.points[i][0]
					if self.points[i][1] > bottom:
						bottom = self.points[i][1]
					if self.points[i][0] > right:
						right = self.points[i][0]
				self.rect = pygame.Rect(left-self.size/2, top-self.size/2-200, right-left + self.size, bottom-top + self.size)
				self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
				self.proportion = self.rect.height/self.rect.width
				if self.checkSinglePoint():
					pygame.draw.circle(self.surface, self.color, (self.points[0][0]-self.rect.x, self.points[0][1]-self.rect.y), self.size/2)
				else:
					i = 0
					for point in self.points:
						if self.tool == 2:
							pygame.draw.circle(self.surface, self.color, (point[0]-self.rect.x, point[1]-200-self.rect.y), self.size/2)
						elif self.tool == 1:
							if i < len(self.points)-1 and i > 1:
								pygame.draw.line(self.surface, self.color, (point[0]-self.rect.x, point[1]-200-self.rect.y), (self.points[i+1][0]-self.rect.x, self.points[i+1][1]-200-self.rect.y), self.size)
						i += 1

				self.scaledSurface = pygame.transform.scale(self.surface, (self.rect.width, self.rect.height))
				# self.scaledSurface = self.surface.copy()

		elif self.tool == 4:
			self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
			pygame.draw.rect(self.surface, self.color, self.rect, self.size)

class Shapes(Stroke):
	def __init__(self, color, size, tool, point):
		super().__init__(color, size, tool)
		self.pos = point
		self.rect = pygame.Rect(point[0], point[1], self.size, self.size)
		self.surface = None
		self.scaledSurface = None
		self.finished = False
	
	def drawStroke(self):
		if self.finished:
			drawingSurface.blit(self.scaledSurface, (self.rect.x, self.rect.y))

		else:
			pos = pygame.mouse.get_pos()
			if tool == 3:
				self.rect = pygame.Rect(self.rect.x, self.rect.y, pos[0]-self.rect.x, pos[1]-self.rect.y-100)
				pygame.draw.rect(drawingSurface, self.color, self.rect, int(self.size))
			if tool == 4:
				self.radius = math.sqrt((pos[0]-self.pos[0])**2 + (pos[1]-self.pos[1]-100)**2)
				pygame.draw.circle(drawingSurface, self.color, (self.pos[0], self.pos[1]), self.radius, int(self.size))

	def makeSurf(self):
		if self.rect.width < 0:
			self.rect.x += self.rect.width
		if self.rect.height < 0:
			self.rect.y += self.rect.height
		
		self.surface = pygame.Surface((abs(self.rect.width), abs(self.rect.height)), pygame.SRCALPHA)
		if tool == 3:
			self.surface = pygame.Surface((abs(self.rect.width), abs(self.rect.height)), pygame.SRCALPHA)
			self.rect.width = abs(self.rect.width)
			self.rect.height = abs(self.rect.height)
			pygame.draw.rect(self.surface, self.color, pygame.Rect(0,0, abs(self.rect.width), abs(self.rect.height)), int(self.size*2))

		if tool == 4:
			self.rect = pygame.Rect(self.pos[0]-self.radius, self.pos[1]-self.radius, self.radius*2, self.radius*2)
			self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
			pygame.draw.circle(self.surface, self.color, (self.rect.width/2, self.rect.height/2), self.rect.width/2, int(self.size))
		self.scaledSurface = self.surface.copy()
		self.proportion = self.rect.height/self.rect.width

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

	def get_rgb(self):
		return (self.red, self.green, self.blue)

	@property 
	def hue(self) -> float:
		return self._hue
    
	@property
	def saturation(self) -> float:
		return self._saturation
	
	@property
	def value(self) -> float:
		return self._value


def colorWheel(radius, value) -> pygame.Surface:
    colorWheel: list[Color] = []
    wheelSurface = pygame.Surface((radius * 2 + 1, radius * 2 + 1), pygame.SRCALPHA)
    wheelSurface = wheelSurface.convert_alpha()
    wheelSurface.fill((0,0,0,0))
    wheelPixels = pygame.PixelArray(wheelSurface)


    for hue in range(360):  
        # for value in range(6):  
        for saturation in range(51):  
            colorWheel.append(Color(hsv=(hue+300, saturation / 50, value)))


    for i in range(len(colorWheel)):
        color = colorWheel[i]
        rads = radians(color.hue)
        pointLength = color.saturation * (radius-1)

        x = 0
        y = 0
        # originX = (color.value * spacing) + radius
        originX = radius
        originY = radius
        
        x = int(pointLength * cos(rads) + originX)
        y = int(pointLength * sin(rads) + originY)
        
        wheelPixels[x,y] = color.rgb
        wheelPixels[x+1,y] = color.rgb
        wheelPixels[x,y+1] = color.rgb
        wheelPixels[x+1,y+1] = color.rgb

    wheelPixels.close()
    return wheelSurface

wheel = colorWheel(100, 1).convert_alpha()
wheel.set_alpha(0)
wheel = pygame.transform.rotate(wheel, 270)
wheel = pygame.transform.flip(wheel, True, False)


running = True
while running:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False
	run(events)
	pygame.display.flip()