from . import Command
from math import floor

COMMANDS = {
    'ON': (Command(0x22, wait=True), #All
          Command(0x22, wait=True), #Group 1
          Command(0x22, wait=True), #Group 2
          Command(0x22, wait=True), #Group 3
          Command(0x22, wait=True)), #Group 4
    'OFF': (Command(0x21), #All
          Command(0x21), #Group 1
          Command(0x21), #Group 2
          Command(0x21), #Group 3
          Command(0x21)), #Group 4
    'BRIGHTER': Command(0x23),
    'DARKER': Command(0x24),
    'DISCOUP': Command(0x27),
    'DISCODOWN': Command(0x28),
    'SLOWER': Command(0x26),
    'FASTER': Command(0x25),
}

PARTIES = { #TODO, get all 20 party modes?
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

def brightest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['BRIGHTER'])
    return tuple(commands)

def darkest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COMMANDS['DARKER'])
    return tuple(commands)

def fade_up(group=0):
    commands = list(darkest(group))
    for i in range(0, 10):
        commands.append(COMMANDS['BRIGHTER'].with_wait(True))
    return tuple(commands)

COMMANDS['FADEUP'] = fade_up
    
def fade_down(group=0):
    commands = list(brightest(group))
    for i in range(0, 10):
        commands.append(COMMANDS['DARKER'].with_wait(True))
    return tuple(commands)

COMMANDS['FADEDOWN'] = fade_down

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Brightness must be value between 0 and 100")
    b = int(floor(level / 10.0)) #lights have 10 levels of brightness
    commands = list(darkest(group))
    for i in range(0, b):
        commands.append(COMMANDS['BRIGHTER'])
    return tuple(commands)

COMMANDS['BRIGHTNESS'] = brightness

def color(hue=0, group=0):
    if hue not in range(0,256):
        raise Exception("Color must be value between 0 and 255")
    return (COMMANDS['ON'][group], Command(0x20, hue))

COMMANDS['COLOR'] = color
    
def partay(mode, group=0):
    if mode not in PARTIES:
        raise Exception("Party Mode %s doesn't exist" % mode)
    number = PARTIES[mode]
    
    commands = [COMMANDS['ON'][group]]
    for i in range(1, number):
        commands.append(COMMANDS['DISCOUP'])
    return tuple(commands)

COMMANDS['PARTY'] = partay