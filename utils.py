from datetime import datetime
from dataclasses import dataclass
import pygame
import os
import random
import numpy
import copy
import math
pygame.font.init()
red = [255,0,0]
pink = [255,0,255]
yellow = [255,255,0]
blue = [0,0,255]
lightBlue = [64,64,255]
orange = [255,165,0]
green = [0,255,0]
purple = [127,0,255]
white = [255,255,255]
lightGray = [192,192,192]
gray = [127,127,127]
darkGray = [64,64,64]
black = [0,0,0]
lightBlueishGray = [169, 204, 200]
lightGreen = [105, 201, 40]
wood = [161, 102, 47]
colors = [red, pink, yellow, blue, orange, green, purple, white, lightGray, gray, darkGray, black, lightBlueishGray, lightBlue, wood]
alphabet = 'abcdefghijklmnopqrstuvwxyz'
class Coordinate():
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, xyz: list[float, float, float] = None, xy: list[float, float] = None) -> None:
        self.x: float
        self.y: float
        self.z: float
        if xyz == None and xy == None:
            self.x = x
            self.y = y
            self.z = z
        elif xy == None:
            self.x, self.y, self.z = xyz
        else:
            if len(xy) <= 2:
                self.x = xy[0]
                self.y = xy[1]
                self.z=0
            else:
                self.x, self.y, self.z = xy
        self.xy = [x,y]
        self.xyi = [int(x), int(y)]
        self.array = numpy.array((self.x, self.y, self.z))
    def Rotate(self, angle: float):
        '''Angle is in Rads'''
        return Coordinate(self.x*math.cos(angle)-self.y*math.sin(angle), self.y*math.cos(angle)+self.x*math.sin(angle))
    def Normalize(self):
        return self/abs(self)
    def toColor(self):
        return (min(self.x*255, 255), min(self.y*255, 255), min(self.z*255, 255))
    def __abs__(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    def __sub__(self, other):
        if other.__class__ == Coordinate:
            return Coordinate(self.x-other.x, self.y-other.y, self.z-other.z)
        else:
            try:
                return Coordinate(self.x-other[0], self.y-other[1], self.z-other[3])
            except:
                return Coordinate(self.x-other[0], self.y-other[1])
    def __add__(self, other):
        if other.__class__ == Coordinate:
            return Coordinate(self.x+other.x, self.y+other.y)
        elif other.__class__ in (list, tuple):
            return Coordinate(self.x+other[0], self.y+other[1])
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'
    def __truediv__(self, other:int | float):
        if other.__class__ == int or other.__class__ == float or other.__class__ == numpy.float64:
            return Coordinate(self.x/other, self.y/other, self.z/other)
        else:
            return self
    def __mul__(self, other):
        '''Not Implemented for Coordinate * Coordinate'''
        if other.__class__ == int or other.__class__ == float or other.__class__ == numpy.float64:
            return Coordinate(self.x*other, self.y*other, self.z*other)
        else:
            return self
    def __neg__(self):
        return Coordinate(-self.x, -self.y)
    def __round__(self, places=None):
        return Coordinate(round(self.x, places), round(self.y, places))
    def __len__(self):
        return 3
    def __iter__(self):
        yield from self.array
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            return None
class Color():
    def __init__(self, rgb: tuple[int, int, int]) -> None:
        self.rgb = rgb
        self.r, self.g, self.b = rgb
    def closeTo(self, other, tolerance):
        return abs(other.r-self.r) < tolerance and abs(other.g-self.g) < tolerance and abs(other.b-self.b) < tolerance
    def __str__(self) -> str:
        return f'({self.r}, {self.g}, {self.b})'
    def __iter__(self):
        yield from self.rgb
def Magnitude(p1: Coordinate | tuple, p2: Coordinate | tuple = None) -> float:
    if p2 == None:
        return math.sqrt(p1[0]**2+p1[1]**2)
    else:
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
def Unitize(start:Coordinate, end:Coordinate) -> Coordinate:
    return ((end-start)/abs(end-start)+start)
def Midpoint(point1, point2):
    if type(point1) == int:
        return (point1+point2)/2
    elif len(point1) == 2:
        midpoint = ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2)
    else:
        midpoint = ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2, (point1[2]+point2[2])/2)
    return midpoint
def Normal(start:Coordinate, end:Coordinate) -> Coordinate:
    dx = end.x-start.x
    dy = end.y-start.y
    m = Midpoint(start, end)
    c = Coordinate(-dy,dx)+m
    return Unitize(m,c)
def intersectTwoCircles(x1,y1,r1, x2,y2,r2):
    centerdx = x1 - x2
    centerdy = y1 - y2
    R = math.sqrt(centerdx * centerdx + centerdy * centerdy)
    if (not (abs(r1 - r2) <= R and R <= r1 + r2)):
        return [] 
    R2 = R*R
    R4 = R2*R2
    a = (r1*r1 - r2*r2) / (2 * R2)
    r2r2 = (r1*r1 - r2*r2)
    c = math.sqrt(2 * (r1*r1 + r2*r2) / R2 - (r2r2 * r2r2) / R4 - 1)

    fx = (x1+x2) / 2 + a * (x2 - x1)
    gx = c * (y2 - y1) / 2
    ix1 = fx + gx
    ix2 = fx - gx

    fy = (y1+y2) / 2 + a * (y2 - y1)
    gy = c * (x1 - x2) / 2
    iy1 = fy + gy
    iy2 = fy - gy
    return [[ix1, iy1], [ix2, iy2]]
def DrawArrow(start: Coordinate, end: Coordinate, surface: pygame.Surface, color:pygame.Color, thickness, method:str):
    if method == "IND":
        pygame.draw.line(surface, color, start, end, width=thickness)
        m = Magnitude(start, end)
        sign = (start.y-end.y)/m if m!=0 else -1
        offset = m/10
        a=-math.atan2(end.y-start.y, end.x-start.x)+math.pi/4
        pygame.draw.line(surface, color, end, end+(offset*math.cos(a), offset*math.sin(a)), width=thickness)
        pygame.draw.line(surface, color, end, end+(-offset*math.cos(a), offset*math.sin(a)), width=thickness)
    elif method == "TOG":
        temp = pygame.Surface(surface.get_size())
        m = Magnitude(start, end)
        offset = m/10
        end2 = start+Coordinate(0, m)
        pygame.draw.line(temp, color, start, end2, width=thickness)
        pygame.draw.line(temp, color, end2, end2+(offset, -offset), width=thickness)
        pygame.draw.line(temp, color, end2, end2+(-offset, -offset), width=thickness)
        a=math.degrees(math.atan2(end.y-start.y, end.x-start.x))-90
        temp = pygame.transform.rotate(temp, -a)
        temp = temp.subsurface(temp.get_bounding_rect())
        surface.blit(temp, (0,0))
def bezier(p1: Coordinate, p2: Coordinate, p3: Coordinate, surface: pygame.Surface, color: pygame.Color | Color, width: int = 1, detail: int = 100) -> None:
    if color.__class__ == Color:
        color = color.rgb
    pxp, pyp = p1
    for t in numpy.linspace(0, 1, detail):
        px = p1[0]*(1-t)**2 + 2*(1-t)*t*p2[0] + p3[0]*t**2
        py = p1[1]*(1-t)**2 + 2*(1-t)*t*p2[1] + p3[1]*t**2       
        pygame.draw.line(surface, color, (pxp,pyp), (px,py), width=width)
        pygame.draw.circle(surface, color, (px, py), width/2, width=0)
        pxp = px
        pyp = py
def TakeScreenshot(surface: pygame.Surface):
    time = datetime.now()
    currentTime = time.strftime("%Y-%m-%d_%H.%M.%S")
    os.makedirs('screenshots', exist_ok=True)
    pygame.image.save(surface, os.path.join('screenshots', f'{currentTime}.png'))
    print(f"Saved Screenshot to {os.path.join('screenshots', f'{currentTime}')}.png")
class Hex():
    def __init__(self, hEx:str):
        self.hex = hEx
        self.rgb = (int('0x'+hEx[0:2],16),int('0x'+hEx[2:4],16),int('0x'+hEx[4:6],16))
def ReplaceColor(surface: pygame.Surface, colorToBeReplaced: pygame.Color | Hex, colorToReplaceWith: pygame.Color):
    temp = copy.copy(surface)
    if colorToBeReplaced.__class__ == Hex:
        colorToBeReplaced = colorToBeReplaced.rgb
    if colorToReplaceWith.__class__ == Hex:
        colorToReplaceWith = colorToReplaceWith.rgb
    for x in range(temp.get_width()):
        for y in range(temp.get_height()):
            if temp.get_at((x, y)) == colorToBeReplaced:
                temp.set_at((x, y), colorToReplaceWith)
    return temp
def WeightedAverageColor(inputs: list[tuple[tuple[int,int,int], float]]):
    weights = [inputs[x][1] for x in range(len(inputs))]
    r = sum([inputs[x][0][0] * weights[x] for x in range(len(weights))])
    g = sum([inputs[x][0][1] * weights[x] for x in range(len(weights))])
    b = sum([inputs[x][0][2] * weights[x] for x in range(len(weights))])
    totalWeights = sum(weights)
    averageColor = (int(r/totalWeights), int(g/totalWeights), int(b/totalWeights))
    return averageColor
def Average(x: list[float]):
    return sum(x)/len(x)
def lerp(a: float, b: float, t: float) -> float:
    'Returns a value inbetween a and b based on t'
    return (1 - t) * a + t * b if t < 1 else b
def lerp2d(a: tuple, b: tuple, t: float) -> tuple:
    return Coordinate(lerp(a[0], b[0], t), lerp(a[1], b[1], t))
def inv_lerp(a: float, b: float, v: float) -> float:
    'Returns a percentage between a and b based on v'
    return (v - a) / (b - a)
def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
    '''Remaps v from i to o
    
    Example 50, 100, 0, 100, 75 would return 50'''
    return lerp(o_min, o_max, inv_lerp(i_min, i_max, v))
def Slider(start: int, length: int, x:int, y: int, screen: pygame.Surface, lineColor: pygame.Color = gray, knobColor: pygame.Color = darkGray, displayText: bool = True, returnPercent: bool = True, name:str = '', outline: pygame.Color = None) -> tuple[float, int]:
    end = start + length
    myFont = pygame.font.Font(None, 25)
    mousePos = pygame.mouse.get_pos()
    pygame.draw.line(screen, lineColor, (start, y), (end, y), width=7)
    slider = pygame.draw.circle(screen, knobColor, (x, y), 10, width=0)
    mouseDown = pygame.mouse.get_pressed()[0]
    if mousePos[1] >= slider.top and mousePos[1] <= slider.bottom and mousePos[0] >= start-10 and mousePos[0] <= end+10 and mouseDown == True:
        x = mousePos[0]
    if x < start:
        x = start
    elif x > end:
        x = end
    if outline:
        pygame.draw.circle(screen, outline, (x, y), 11, width=0)
    slider = pygame.draw.circle(screen, knobColor, (x, y), 10, width=0)
    value = x-start
    percent = round(remap(start, end, 0, 100, x))/100
    if displayText and not returnPercent:
        text = myFont.render(str(f'{value}'), True, lineColor)
        screen.blit(text, (x-text.get_width()+10/2, y-30))
        if name != '':
            text = myFont.render(name, True, lineColor)
            screen.blit(text, (end+10, y-text.get_height()/2))
    elif displayText and returnPercent:
        text = myFont.render(str(f'{round(percent*100)}%'), True, lineColor)
        screen.blit(text, (x-text.get_width()+10/2, y-30))
        if name != '':
            text = myFont.render(name, True, lineColor)
            screen.blit(text, (end+10, y-text.get_height()/2))
    if returnPercent:
        return percent, x
    return value, x
def dithering(ditheringArea: pygame.Rect, surface: pygame.Surface, color1, color2, offset: int, direction:str):
    random.seed(1)
    for x in range(ditheringArea.left, ditheringArea.right):
        for y in range(ditheringArea.top, ditheringArea.bottom):
            if direction == 'H':
                surface.set_at((x,y), color1 if random.randint(ditheringArea.left+offset, ditheringArea.right-offset) < x else color2)
            elif direction == 'V':
                surface.set_at((x,y), color1 if random.randint(ditheringArea.top+offset, ditheringArea.bottom-offset) < y else color2)
def TriangleMidpoint(point1, point2, point3):
    if len(point1) == 2:
        midpoint = ((point1[0]+point2[0]+point3[0])/3, (point1[1]+point2[1]+point3[1])/3)
    else:
        midpoint = ((point1[0]+point2[0]+point3[0])/3, (point1[1]+point2[1]+point3[1])/3, (point1[2]+point2[2]+point3[2])/3)
    return numpy.array(midpoint)
def TextInput(name: str, text: str, event: pygame.event.Event | None, color: pygame.Color, surface: pygame.Surface, pos: Coordinate):
    font = pygame.font.Font(None, int(surface.get_size()[0]/10))
    texty = font.render(f'{name}: ', True, color)
    surface.blit(texty, pos)
    if event:
        key = event.__dict__['unicode']
        text += key
    texty2 = font.render(text, True, color)
    surface.blit(texty2, (pos[0]+texty.get_width(), pos[1]))
    return text
def Arrows(optionName: str, options: list, color: pygame.Color, optionNum: int, surface: pygame.Surface, pos: tuple[int, int], cooldown: int, font = None):
    if font == None:
        font = pygame.font.Font(None, int(surface.get_size()[0]/20))
    optionOffset = 30
    cool = False if cooldown == 0 else True
    mousePos = pygame.mouse.get_pos()
    text = font.render(optionName+':', True, color)
    surface.blit(text, pos)
    text2 = font.render(str(options[optionNum-1]), True, color)
    surface.blit(text2, (pos[0]+text.get_width()+optionOffset, pos[1]))
    pos0 = pos[0]+text.get_width()+optionOffset-5
    pos1 = pos[1]+5
    left = pygame.draw.polygon(surface, color, [(pos0, pos1), (pos0-5, pos1), (pos0-15, pos1+10), (pos0-5, pos1+20), (pos0, pos1+20), (pos0-10, pos1+10)])
    pos0 = pos[0]+text.get_width()+optionOffset+text2.get_width()+5
    pos1 = pos[1]+5
    right = pygame.draw.polygon(surface, color, [(pos0, pos1), (pos0+5, pos1), (pos0+15, pos1+10), (pos0+5, pos1+20), (pos0, pos1+20), (pos0+10, pos1+10)])
    if pygame.mouse.get_pressed()[0] and cooldown == 0:
        if pygame.Rect.colliderect(pygame.Rect(mousePos, (1,1)), left):
            optionNum -= 1
            cool = True
        elif pygame.Rect.colliderect(pygame.Rect(mousePos, (1,1)), right):
            optionNum += 1
            cool = True
    if optionNum < 1:
        optionNum = len(options)
    elif optionNum > len(options):
        optionNum = 1
    if cool == True:
        cooldown += 1
    if cooldown >= 10:
        cooldown = 0
        cool = False
    return optionNum, options[optionNum-1], cooldown
def Mouseover(mousePos:Coordinate, object:pygame.Rect):
    return object.colliderect(mousePos, (1,1))
@dataclass
class Colors():
    white = white
class Setting():
    'Not fully implemented'
    class Slider():
        'Not yet implemented'
        def __init__(self, start, length, x, y) -> None:
            self.start = start
            self.length = length
            self.x = x
            self.y = y
    class Dropdown():
        "Put 'Event' in event handler under MOUSEBUTTONDOWN"
        def __init__(self, options: list, color: pygame.Color, hoverColor: pygame.Color, textColor: pygame.Color) -> None:
            "Put 'Event' in event handler under MOUSEBUTTONDOWN"
            self.color = color
            self.hoverColor = hoverColor
            self.textColor = textColor
            self.options = options
            self.selected = 0
            self.opened = False
            self.found = False
        def Render(self, surface: pygame.Surface, pos:Coordinate, mousePos:Coordinate, size:int | tuple[int, int]):
            "Put 'Event' in event handler under MOUSEBUTTONDOWN"
            font = pygame.font.SysFont('arialbold', 20)
            textSizesX = [1]
            textSizesY = [1]
            if size.__class__ == int and self.found == False:
                font = pygame.font.SysFont('arialbold', int(size*1.25))
                self.fontSize = size*1.25
                self.found = True
                textSizesX = []
                textSizesY = []
                for option in self.options:
                    text = font.render(str(option), True, self.textColor)
                    textSizesX.append(text.get_width())
                    textSizesY.append(text.get_height())
                self.dropdown = pygame.Rect((pos, (max(textSizesX)+ max(textSizesY)+4, max(textSizesY)+4)))
            elif self.found == False:
                fontSize = 1
                while True:
                    textSizesX = []
                    textSizesY = []
                    font = pygame.font.SysFont('arialbold', fontSize)
                    for option in self.options:
                        text = font.render(str(option), True, self.textColor)
                        textSizesX.append(text.get_width())
                        textSizesY.append(text.get_height())
                    if max(textSizesX) >= size[0]-size[1]:
                        self.fontSize = fontSize-1
                        self.found = True
                        break
                    fontSize += 1
                font = pygame.font.SysFont('arialbold', self.fontSize)
                self.dropdown = pygame.Rect((pos, size))
            if Mouseover(mousePos, self.dropdown):
                pygame.draw.rect(surface, lightGray, self.dropdown, width=0)
            else:
                pygame.draw.rect(surface, gray, self.dropdown, width=0)
            text = font.render(str(self.options[self.selected]), True, white)
            surface.blit(text, (self.dropdown.left+2, self.dropdown.top+2))
            self.dropdownOptions = []
            if self.opened:
                pygame.draw.line(surface, white, (self.dropdown.right-5, self.dropdown.bottom-5), (self.dropdown.right-(self.dropdown.height/2), self.dropdown.top+5), width=2)
                pygame.draw.line(surface, white, (self.dropdown.right-(self.dropdown.height/2), self.dropdown.top+5), (self.dropdown.right-self.dropdown.height+5, self.dropdown.bottom-5), width=2)
                for i, option in enumerate(self.options):
                    text = font.render(str(option), True, white)
                    self.dropdownOption = pygame.Rect(self.dropdown.left, self.dropdown.bottom+self.dropdown.height*i, self.dropdown.width, self.dropdown.height)
                    self.dropdownOptions.append(pygame.draw.rect(surface, gray, self.dropdownOption, width=0))
                    surface.blit(text, (self.dropdownOption.left+2, self.dropdownOption.top+2))
                    pygame.draw.rect(surface, darkGray, self.dropdownOption, width=1)
            else:
                pygame.draw.line(surface, white, (self.dropdown.right-5, self.dropdown.top+5), (self.dropdown.right-(self.dropdown.height/2), self.dropdown.bottom-5), width=2)
                pygame.draw.line(surface, white, (self.dropdown.right-(self.dropdown.height/2), self.dropdown.bottom-5), (self.dropdown.right-self.dropdown.height+5, self.dropdown.top+5), width=2)
        def Event(self, event: pygame.event.Event):
            if Mouseover(event.__dict__['pos'], self.dropdown):
                self.opened = not self.opened
            if self.opened:
                for i, option in enumerate(self.dropdownOptions):
                    if Mouseover(event.__dict__['pos'], option):
                        self.selected = i
                        self.opened = False
            return self.selected
    class Checkbox():
        "Put 'Event' in event handler under MOUSEBUTTONDOWN"
        def __init__(self, pos: Coordinate, size: int, text: str) -> None:
            "Put 'Event' in event handler under MOUSEBUTTONDOWN"
            self.pos = pos
            self.size = size
            self.text = str(text)
            self.checked = False
        def Render(self, surface, color):
            "Put 'Event' in event handler under MOUSEBUTTONDOWN"
            pygame.draw.rect(surface, color, (self.pos, (self.size, self.size)), width=1, border_radius=int(self.size/10))
            font = pygame.font.SysFont('calibri', int(self.size*1.25), bold=False, italic=False)
            text = font.render(self.text, True, color)
            surface.blit(text, (self.pos[0]+self.size+5, self.pos[1]-1))
            if self.checked:
                pygame.draw.line(surface, color, (self.pos[0]+2, self.pos[1]+(self.size/5)), (self.pos[0]+(self.size/2), self.pos[1]+self.size*.75), width=3)
                pygame.draw.line(surface, color, (self.pos[0]+(self.size/2), self.pos[1]+self.size*.75), (self.pos[0]+self.size*1.1, self.pos[1]-self.size*.1), width=3)
        def Event(self, event):
            if (event.__dict__['pos'][0] > self.pos[0] and event.__dict__['pos'][0] < self.pos[0]+self.size) and (event.__dict__['pos'][1] > self.pos[1] and event.__dict__['pos'][1] < self.pos[1]+self.size):
                self.checked = not self.checked
    class Arrows():
        'Not yet implemented'
        def __init__(self) -> None:
            pass
    class Button():
        "Put 'Clicked' in event handler under MOUSEBUTTONDOWN"
        def __init__(self, color:pygame.Color, mouseOverColor:pygame.Color, clickedColor: pygame.Color, textColor:pygame.Color, text:str) -> None:
            "Put 'Clicked' in event handler under MOUSEBUTTONDOWN"
            self.color = color
            self.mouseOverColor = mouseOverColor
            self.textColor = textColor
            self.text = str(text)
            self.sidePadding = 3
            self.topPadding = 1
            self.clickedColor = clickedColor
        def Render(self, surface:pygame.Surface, pos:Coordinate, size:int, mousePos:Coordinate):
            "Put 'Clicked' in event handler under MOUSEBUTTONDOWN"
            self.pos = pos
            self.size = size
            self.surface = surface
            font = pygame.font.SysFont('arialbold', 20)
            text = font.render(self.text, True, self.textColor)
            textSize = text.get_size()
            self.textSize = textSize
            self.rect = pygame.Rect(pos, (textSize[0]+self.sidePadding*2, textSize[1]+self.topPadding*2))
            if Mouseover(mousePos, self.rect):
                pygame.draw.rect(surface, self.mouseOverColor, (pos, (textSize[0]+self.sidePadding*2, textSize[1]+self.topPadding*2)), width=0)
            else:
                pygame.draw.rect(surface, self.color, (pos, (textSize[0]+self.sidePadding*2, textSize[1]+self.topPadding*2)), width=0)
            surface.blit(text, (pos[0]+self.sidePadding, pos[1]+self.topPadding))
        def Clicked(self, event:pygame.event.Event):
            clicked = (event.__dict__['pos'][0] > self.pos[0] and event.__dict__['pos'][0] < self.pos[0]+self.textSize[0]+self.sidePadding*2) and (event.__dict__['pos'][1] > self.pos[1] and event.__dict__['pos'][1] < self.pos[1]+self.textSize[1]+self.topPadding*2)
            if clicked:
                pygame.draw.rect(self.surface, self.clickedColor, self.rect, width=0)
                return True
            else:
                return False