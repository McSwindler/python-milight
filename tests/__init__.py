import unittest
import milight.rgbw, milight.white

class TestRgbwLights(unittest.TestCase):
    def setUp(self):
        self.led = milight.MiLight("127.0.0.1", wait_duration=0)

    def test_default_constructor(self):
        led = milight.MiLight("127.0.0.1")
        self.assertEqual(led._address, "127.0.0.1")
        self.assertEqual(led._port, 8899)
        self.assertEqual(led._wait, 0.025)

    def test_changing_port(self):
        led = milight.MiLight("127.0.0.1", port=50000)
        self.assertEqual(led._port, 50000)

    def test_sleep(self):
        led = milight.MiLight("127.0.0.1")
        led.send(milight.rgbw.ON[0])
        led.send(milight.rgbw.OFF[0])

    def test_changing_pause(self):
        led = milight.MiLight("127.0.0.1", wait_duration=0.8)
        self.assertEqual(led._wait, 0.8)

    def test_on(self):
        self.led.send(milight.rgbw.ON[0])
        self.led.send(milight.rgbw.ON[1])

    def test_off(self):
        self.led.send(milight.rgbw.OFF[0])
        self.led.send(milight.rgbw.OFF[1])

    def test_white(self):
        for i in range(0,5):
            self.led.send(milight.rgbw.WHITE[i])

    def test_set_color(self):
        self.led.send(milight.rgbw.color(0))
        self.led.send(milight.rgbw.color(127, 1))
        self.led.send(milight.rgbw.color_from_rgb(0xff, 0, 127))
        self.led.send(milight.rgbw.color_from_hls(0.5, 0.5, 0.5, 1))

    def test_set_brightness(self):
        self.led.send(milight.rgbw.brightness(50))
        self.led.send(milight.rgbw.brightness(50, 1))

    def test_party_mode(self):
        self.led.send(milight.rgbw.party_mode('random'))

    def test_disco_faster(self):
        self.led.send((milight.rgbw.ON[1], milight.rgbw.SPEED_UP))

    def test_disco_slower(self):
        self.led.send((milight.rgbw.ON[1], milight.rgbw.SLOW_DOWN))
