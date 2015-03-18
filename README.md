# MiLight Controller
This is a controller for the following brands of light bulbs:
* MiLight
* LimitlessLED
* AppLight
* AppLamp
* LEDme
* dekolight
* iLight
* EasyBulb

# Installation
```.py
pip install milight
```

# Usage
```.py
import milight.rgbw
light = milight.MiLight('192.168.0.12')
light.send(milight.rgbw.ON[1]) # Turn on the lights in group 1
light.send(milight.rgbw.color_from_rgb(0xff, 0x00, 0x00, 1)) # Change the color to Red
light.send(milight.rgbw.brightness(0, 1)) # Set to the lowest brightness
light.send(milight.rgbw.fade_up(1)) # fade up and down
light.send(milight.rgbw.fade_down(1)) 
light.send(milight.rgbw.OFF[1]) # turn off
```

# Notes
* You must first setup your WiFi bridge and sync/pair the light bulbs you want in each group.
* By default, there is a .025s wait between each command. This can be changed on init by setting the `wait_duration` parameter