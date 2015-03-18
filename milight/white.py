from . import Command
from math import floor
import colorsys

COMMANDS = {
    'ON': (Command(0x35, wait=True), #All
          Command(0x38, wait=True), #Group 1
          Command(0x3D, wait=True), #Group 2
          Command(0x37, wait=True), #Group 3
          Command(0x32, wait=True)), #Group 4
    'OFF': (Command(0x39), #All
          Command(0x3B), #Group 1
          Command(0x33), #Group 2
          Command(0x3A), #Group 3
          Command(0x36)), #Group 4
}

WHITE = ((COMMANDS['ON'][0], Command(0xB5)), #All
      (COMMANDS['ON'][1], Command(0xB8)), #Group 1
      (COMMANDS['ON'][2], Command(0xBD)), #Group 2
      (COMMANDS['ON'][3], Command(0xB7)), #Group 3
      (COMMANDS['ON'][4], Command(0xB2))) #Group 4

NIGHT = ((COMMANDS['OFF'][0], Command(0xB9)), #All
      (COMMANDS['OFF'][1], Command(0xBB)), #Group 1
      (COMMANDS['OFF'][2], Command(0xB3)), #Group 2
      (COMMANDS['OFF'][3], Command(0xBA)), #Group 3
      (COMMANDS['OFF'][4], Command(0xB6))) #Group 4

BRIGHTER = Command(0x3C)
DARKER = Command(0x34)

WARMER = Command(0x3E)
COOLER = Command(0x3F)

def brightest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(BRIGHTER)
    return WHITE[group]

def darkest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(DARKER)
    return tuple(commands)

def warmest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(WARMER)
    return tuple(commands)

def coolest(group=0):
    commands = [COMMANDS['ON'][group]]
    for i in range(0, 10):
        commands.append(COOLER)
    return tuple(commands)

def fade_up(group=0):
    commands = list(darkest(group))
    for i in range(0, 10):
        commands.append(Command(0x3C, wait=True))
    return tuple(commands)
    
def fade_down(group=0):
    commands = []
    for i in range(0, 10):
        commands.append(Command(0x3C, wait=True))
    return brightest(group) + tuple(reversed(commands))

def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Brightness must be value between 0 and 100")
    b = int(floor(level / 10.0)) #lights have 10 levels of brightness
    commands = list(darkest(group))
    for i in range(0, b):
        commands.append(BRIGHTER)
    return tuple(commands)

def warmness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Warmness must be value between 0 and 100")
    b = int(floor(level / 10.0)) #lights have 10 levels of warmness
    commands = list(coolest(group))
    for i in range(0, b):
        commands.append(COMMANDS['WARMER'])
    return tuple(commands)

def color(*kwargs):
    return None