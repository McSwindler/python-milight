from . import Command
from math import floor

COMMANDS = {
    'ON': (Command(0x42, wait=True), #All
          Command(0x45, wait=True), #Group 1
          Command(0x47, wait=True), #Group 2
          Command(0x49, wait=True), #Group 3
          Command(0x4B, wait=True)), #Group 4
    'OFF': (Command(0x41), #All
          Command(0x46), #Group 1
          Command(0x48), #Group 2
          Command(0x4A), #Group 3
          Command(0x4C)), #Group 4
    'DISCO': Command(0x4D),
    'SLOWER': Command(0x43),
    'FASTER': Command(0x44),
}

COMMANDS['WHITE'] = ((COMMANDS['ON'][0], Command(0xC2)), #All
          (COMMANDS['ON'][1], Command(0xC5)), #Group 1
          (COMMANDS['ON'][2], Command(0xC7)), #Group 2
          (COMMANDS['ON'][3], Command(0xC9)), #Group 3
          (COMMANDS['ON'][4], Command(0xCB))) #Group 4
          
COMMANDS['SYNC'] = (None, #All
          COMMANDS['ON'][1].with_repeat(5), #Group 1
          COMMANDS['ON'][2].with_repeat(5), #Group 2
          COMMANDS['ON'][3].with_repeat(5), #Group 3
          COMMANDS['ON'][4].with_repeat(5)) #Group 4

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

def fade_up(group=0):
    commands = []
    for i in range(2, 28):
        commands.append(Command(0x4E, i, True))
    return tuple(commands)

COMMANDS['FADEUP'] = fade_up
    
def fade_down(group=0):
    return reversed(fade_up(group))

COMMANDS['FADEDOWN'] = fade_down

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Brightness must be value between 0 and 100")
    b = int(floor(level / 4.0) + 2) #lights want values 2-27
    return (COMMANDS['ON'][group], Command(0x4E, b))

COMMANDS['BRIGHTNESS'] = brightness

def color(hue=0, group=0):
    if hue not in range(0,256):
        raise Exception("Color must be value between 0 and 255")
    return (COMMANDS['ON'][group], Command(0x40, hue))

COMMANDS['COLOR'] = color
    
def partay(mode, group=0):
    if mode not in PARTIES:
        raise Exception("Party Mode %s doesn't exist" % mode)
    number = PARTIES[mode]
    
    commands = list(COMMANDS['WHITE'][group])
    for i in range(1, number):
        commands.append(COMMANDS['DISCO'])
    return tuple(commands)

COMMANDS['PARTY'] = partay