import socket, time, colorsys, math, struct

def hex_to_rgb(value):
    if "#" in value:
        value = value[1:]
    return struct.unpack('BBB',value.decode('hex'))

class MiLight:
    def __init__(self, address, port=8899, wait_duration=0.025):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = address
        self._port = port
        self._wait = max(wait_duration, 0)
        
    def send(self, commands):
        if not hasattr(commands, '__iter__'):
            commands = (commands, )
            
        for c in commands:
            for i in range(0, c.repititions()):
                self._sock.sendto(c.message(), (self._address, self._port))
            c.wait()
            time.sleep(self._wait)
            

class Command:
    def __init__(self, b1, b2=0x00, wait=False, repeat=1):
        self._b1 = b1
        self._b2 = b2
        self._wait = wait
        self._repeat = max(repeat, 1)
    
    def message(self):
        return bytearray([self._b1, self._b2, 0x55])

    def wait(self):
        if self._wait:
            time.sleep(0.1)
            
    def set_repeat(self, repeat):
        self._repeat = repeat
    
    def repititions(self):
        return self._repeat