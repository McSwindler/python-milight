import socket, time, struct, threading, binascii
from uuid import uuid4
from math import floor
from colorsys import rgb_to_hls
from importlib import import_module

def color_from_hls(hue, light, sat):
    """ Takes a hls color and converts to proper hue 
        Bulbs use a BGR order instead of RGB """
    if light > 0.95: #too bright, let's just switch to white
        return 256
    elif light < 0.05: #too dark, let's shut it off
        return -1
    else:
        hue = (-hue + 1 + 2.0/3.0) % 1 # invert and translate by 2/3
        return int(floor(hue * 256))

def color_from_rgb(red, green, blue):
    """ Takes your standard rgb color 
        and converts it to a proper hue value """
    
    r = min(red, 255)
    g = min(green, 255)
    b = min(blue, 255)
    if r > 1 or g > 1 or b > 1:
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0

    return color_from_hls(*rgb_to_hls(r,g,b))

def color_from_hex(value):
    """ Takes an HTML hex code
        and converts it to a proper hue value """
    if "#" in value:
        value = value[1:]
    
    try:
        unhexed = bytes.fromhex(value)
    except:
        unhexed = binascii.unhexlify(value) # Fallback for 2.7 compatibility
    return color_from_rgb(*struct.unpack('BBB',unhexed))

class MiLight:
    def __init__(self, hosts={'host': '127.0.0.1', 'port': 8899}, wait_duration=0.025):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._hosts = self._standardize_hosts(hosts)
        self._wait = max(wait_duration, 0)
        self._threads = {}
    
    def __del__(self):
        for t in self._threads:
            self.cancel(t)
        self._sock.close()
        
    def _standardize_hosts(self, hosts):
        if type(hosts) is str:
            hosts = ({'host': hosts}, )
        if type(hosts) is dict:
            hosts = (hosts, )
        temp = []
        for h in hosts:
            default = {'host': '127.0.0.1', 'port': 8899}
            default.update(h)
            temp.append(default)
        return tuple(temp)
    
    def repeat(self, commands, reps=0):
        key = uuid4()
        t = EffectThread(self, commands, reps)
        self._threads[key] = t
        t.start()
        return key
    
    def cancel(self, key):
        t = self._threads.get(key, None)
        if t is not None:
            t.join()
        
    def send(self, commands):
        if not hasattr(commands, '__iter__'):
            commands = (commands, )
            
        for c in commands:
            for h in self._hosts:
                for i in range(0, c.repititions()):
                    self._sock.sendto(c.message(), (h['host'], h['port']))
            c.wait()
            time.sleep(self._wait)
            
class EffectThread(threading.Thread):
    def __init__(self, led, commands, reps=0):
        super(EffectThread, self).__init__()
        self._led = led
        self._commands = commands
        self._reps = reps
        self._running = True

    def run(self):
        count = 1
        while self._running:
            self._led.send(self._commands)
            if self._reps > 0 and count > self._reps:
                break
            count += 1
             
    def join(self):
        self._running = False
        super(EffectThread, self).__init__()

class LightBulb:
    def __init__(self, types=('rgbw', 'white', 'rgb')):
        if type(types) is str:
            types = (types, )
        self._types = []
        for t in types:
            try:
                self._types.append(import_module('.' + t, 'milight'))
            except ImportError:
                print('Unsupported bulb type: %s' % t)
    
    def _concat_command(self, key, idx=None, params=()):
        if idx is not None and idx not in range(0,5):
            raise Exception("Group must be between 0(all) and 4")
        commands = ()
        for type in self._types:
            c = type.COMMANDS.get(key, None)
            if c is None:
                continue;
            if idx is not None:
                c = c[idx]
            if hasattr(c, '__call__'):
                c = c(*params)
            if isinstance(c, Command):
                c = (c,)
            commands += tuple(c)
        return commands
    
    def sync(self, group):
        if group not in range(1,5):
            raise Exception("Group must be between 1 and 4")
        return self._concat_command('SYNC', idx=group)
        
    def on(self, group):
        return self._concat_command('ON', idx=group)
    def all_on(self):
        return self.on(0)
    def off(self, group):
        return self._concat_command('OFF', idx=group)
    def all_off(self):
        return self.off(0)
    def white(self, group=0):
        return self._concat_command('WHITE', idx=group)
    def night(self, group=0):
        return self._concat_command('NIGHT', idx=group)
    def color(self, hue=0, group=0):
        if hue < 0:
            return self.off(group)
        elif hue > 255:
            return self.white(group)
        else:
            return self._concat_command('COLOR', params=(hue, group))
    def brightness(self, level=0, group=0):
        if level not in range(0,101):
            raise Exception("Brightness must be value between 0 and 100")
        return self._concat_command('BRIGHTNESS', params=(level, group))
    def warmness(self, level=0, group=0):
        if level not in range(0,101):
            raise Exception("Warmness must be value between 0 and 100")
        return self._concat_command('WARMNESS', params=(level, group))
    def fade_up(self, group=0):
        return self.on(group) + self._concat_command('FADEUP', params=(group,))
    def fade_down(self, group=0):
        return self.off(group) + self._concat_command('FADEDOWN', params=(group,))
    def party(self, mode, group=0):
        return self._concat_command('PARTY', params=(mode, group))
    def faster(self, group=0):
        return self.on(group) + self._concat_command('FASTER')
    def slower(self, group=0):
        return self.on(group) + self._concat_command('SLOWER')
    def wait(self, sec=0.1):
        """ Wait for x seconds
            each wait command is 100ms """
        sec = max(sec, 0)
        reps = int(floor(sec / 0.1))
        commands = []
        for i in range(0, reps):
            commands.append(Command(0x00, wait=True))
        return tuple(commands)

class Command:
    def __init__(self, b1, b2=0x00, wait=False, repeat=1):
        self._b1 = b1
        self._b2 = b2
        self._wait = wait
        self._repeat = max(repeat, 1)
    
    def message(self):
        return bytearray([self._b1, self._b2, 0x55])
    
    def with_wait(self, wait):
        self._wait = wait
        return self

    def wait(self):
        if self._wait:
            time.sleep(0.1)
            
    def with_repeat(self, repeat):
        self._repeat = max(repeat, 1)
        return self
    
    def repititions(self):
        return self._repeat