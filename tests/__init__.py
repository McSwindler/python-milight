import unittest, time
import milight.rgbw, milight.white

class TestRgbwLights(unittest.TestCase):
    def setUp(self):
        self.led = milight.MiLight("127.0.0.1", wait_duration=0)
        self.bulb = milight.LightBulb('rgbw')

    def test_default_constructor(self):
        led = milight.MiLight({'host': '127.0.0.1'})
        self.assertEqual(led._hosts, ({'host': "127.0.0.1", 'port': 8899},))
        self.assertEqual(led._wait, 0.025)

    def test_changing_port(self):
        led = milight.MiLight({'host': "127.0.0.1", 'port': 50000})
        self.assertEqual(led._hosts, ({'host': "127.0.0.1", 'port': 50000},))

    def test_changing_pause(self):
        led = milight.MiLight({'host': '127.0.0.1'}, wait_duration=0.8)
        self.assertEqual(led._wait, 0.8)

    def test_bulb_concatenation(self):
        led = milight.MiLight({'host': '127.0.0.1'})
        bulb = milight.LightBulb(['rgbw', 'white'])
        commands = bulb.all_on()
        self.assertTupleEqual(commands, (milight.rgbw.COMMANDS['ON'][0], milight.white.COMMANDS['ON'][0]))
        led.send(commands)
        commands = bulb.all_off()
        self.assertTupleEqual(commands, (milight.rgbw.COMMANDS['OFF'][0], milight.white.COMMANDS['OFF'][0]))
        led.send(commands)

    def test_on(self):
        self.led.send(self.bulb.on(0))
        self.led.send(self.bulb.on(1))

    def test_off(self):
        self.led.send(self.bulb.off(0))
        self.led.send(self.bulb.off(1))

    def test_white(self):
        white = self.bulb.white(1)
        color = self.bulb.color(milight.color_from_hls(0.66,1,0.5), 1)
        self.assertEqual(white, color)
        self.led.send(white)

    def test_set_color(self):
        self.led.send(self.bulb.color(0))
        self.led.send(self.bulb.color(127, 1))
        red = milight.color_from_hex('#FF0000')
        self.assertEqual(red, 170)
        self.led.send(self.bulb.color(red))
        blue = milight.color_from_hls(0.66,0.5,0.5)
        self.assertEqual(blue, 1)
        self.led.send(self.bulb.color(blue))

    def test_set_brightness(self):
        self.led.send(self.bulb.brightness(50))
        self.led.send(self.bulb.brightness(50, 1))

    def test_party_mode(self):
        self.led.send(self.bulb.party('random'))

    def test_disco_faster(self):
        self.led.send(self.bulb.faster())

    def test_disco_slower(self):
        self.led.send(self.bulb.slower(1))
        
    def test_fade(self):
        self.led.send(self.bulb.fade_up())
        self.led.send(self.bulb.fade_down())
        
    def test_repetitions(self):
        commands = self.bulb.fade_up() + self.bulb.fade_down()
        key = self.led.repeat(commands)
        time.sleep(10)
        self.led.cancel(key)
        
    def test_wait(self):
        self.led.send(self.bulb.wait(1))
        
    def test_not_supported(self):
        self.assertEqual(self.bulb.warmness(50, 1), ())
