from . import Command
from math import floor
import colorsys

ON = (Command(0x42, wait=True), #All
      Command(0x45, wait=True), #Group 1
      Command(0x47, wait=True), #Group 2
      Command(0x49, wait=True), #Group 3
      Command(0x4B, wait=True)) #Group 4
OFF = (Command(0x41), #All
      Command(0x46), #Group 1
      Command(0x48), #Group 2
      Command(0x4A), #Group 3
      Command(0x4C)) #Group 4

WHITE = ((ON[0], Command(0xC2)), #All
      (ON[1], Command(0xC5)), #Group 1
      (ON[2], Command(0xC7)), #Group 2
      (ON[3], Command(0xC9)), #Group 3
      (ON[4], Command(0xCB))) #Group 4

DISCO = Command(0x4D)
SLOW_DOWN = Command(0x43)
SPEED_UP = Command(0x44)

PARTIES = {
    'white': 1,
    'rainbow_swirl': 2,
    'white_fade': 3,
    'rgbw_fade': 4,
    'rainbow_jump': 5,
    'random': 6,
    'red_twinkle': 7,
    'green_twinkle': 8,
    'blue_twinkle': 9
}

def sync(group):
    if group not in range(1,5):
        raise Exception("Group must be value 1-4")
    return ON[group]

def fade_up(group=0):
    commands = []
    for i in range(2, 28):
        commands.append(Command(0x4E, i, True))
    return tuple(commands)
    
def fade_down(group=0):
    return reversed(fade_up(group))

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level != 0 and floor(level) == 0: #tests for 0-1 values
        level = int(level * 100)
        
    if level not in range(0,101):
        raise Exception("Brightness must be value between 0 and 100")
    b = int(floor(level / 4.0) + 2) #lights want values 2-27
    return Command(0x4E, b)

def color(hue=0, group=0):
    return (ON[group], Command(0x40, hue))

def color_from_hls(hue, light, sat, group=0):
    if light > 0.95: #too bright, let's just switch to white
        return WHITE[group]
    elif light < 0.05: #too dark, let's shut it off
        return WHITE[group] + (brightness(0, group), )
    else: 
        rgb = colorsys.hls_to_rgb(hue, light, sat) #Change the order, best way I could think how
        hsl = colorsys.rgb_to_hls(rgb[2], rgb[1], rgb[0])
        c = int(floor(hsl[0] * 255))
        return color(c, group)
    
    

def color_from_rgb(red, green, blue, group=0):
    """ Takes your standard rgb color 
        and converts it to a proper hue value
        
        the bulbs appear to use bgr"""
    
    r = min(red, 255)
    if r != 0 and floor(r) != 0: #tests for 0-1 values vs 0-255
        r = r / 255.0
    
    g = min(green, 255)
    if g != 0 and floor(g) != 0:
        g = g / 255.0
        
    b = min(blue, 255)
    if b != 0 and floor(b) != 0:
        b = b / 255.0
        
    return color_from_hls(*colorsys.rgb_to_hls(r,g,b))
    
def party_mode(mode, group=0):
    if mode not in PARTIES:
        raise Exception("Party Mode %s doesn't exist" % mode)
    number = PARTIES[mode]
    
    commands = list(WHITE[group])
    for i in range(1, number):
        commands.append(DISCO)
    return tuple(commands)

    #print ('Party mode set.')