# MiLight Controller [![Build Status](https://travis-ci.org/McSwindler/python-milight.svg?branch=master)](https://travis-ci.org/McSwindler/python-milight)
This is a controller for the following brands of light bulbs:
* MiLight
* LimitlessLED
* AppLight
* AppLamp
* LEDme
* dekolight
* iLight
* EasyBulb
Full API documentation can be found here: http://www.limitlessled.com/dev/

# Installation
```.py
pip install milight
```

# Usage
```.py
import milight
controller = milight.MiLight({'host': '127.0.0.1', 'port': 8899}, wait_duration=0) #Create a controller with 0 wait between commands
light = milight.LightBulb(['rgbw', 'white', 'rgb']) #Can specify which types of bulbs to use
controller.send(light.on(1)) # Turn on group 1 lights
controller.send(light.all_on()) # Turn on all lights, equivalent to light.on(0)

""" Colors -
	light.color() takes a hue value 0-255
	this hue can be derived from several helper functions as follows:
	milight.color_from_hls(0.5, 0.5, 0.5)
	milight.color_from_rgb(255, 0, 0)
	milight.color_from_hex('#00ff00') """
controller.send(light.color(milight.color_from_rgb(0xff, 0x00, 0x00), 1)) # Change group 1 color to Red
controller.send(light.white(1)) # Set Group 1 to white
controller.send(light.night(1)) # Set Group 1 to Nightlight mode (white bulbs only)

controller.send(light.brightness(50, 1)) # Set group 1 to half brightness 
controller.send(light.warmness(50, 1)) # Set group 1 to medium heat (white bulbs only)
controller.send(light.fade_up(1)) # fade up group 1
controller.send(light.fade_down(1)) # fade down group 1 

""" Party (Disco) -
	There are 10 party modes available for rgbw and rgb bulbs.
	(There are supposed to be 20 modes for rgb, but I don't have these bulbs to test
		and get the appropriate descriptions. And these bulbs aren't sold anymore)
	To get an idea of all the possible modes, refer to milight.rgbw.PARTIES or milight.rgb.PARTIES """
controller.send(light.party('random', 1)) # Set group 1 to random party (disco) mode
controller.send(light.faster(1)) # Speed up the party effect
controller.send(light.slower(1)) # Slow down the party effect

""" Custom Effects -
	The milight controller has supports to create repetitive commands and run them in a thread.
	The following is an example of fading in and out for 10 seconds. 
	You can also specify the # of repetitions by adjusting the reps parameter. (anything < 0 is infinite) """
import time
commands = light.fade_up() + light.fade_down()
key = controller.repeat(commands, reps=0) # start the effect thread
time.sleep(10)
controller.cancel(key) # stops the effect thread with given key
light.wait(1) # This returns an empty command set that will wait for 1 second, useful for custom effects

controller.send(light.off(1)) # Turn off group 1 lights
controller.send(light.all_off()) # Turn off all lights, equivalent to light.off(0)
```

You can find the raw commands with in the specific bulb modules under the dictionary `COMMANDS`. This contains some single Command objects as well as Command tuples and even some functions. Be cautious when using these values that they are the correct type you need.
Any of the above functions that specify a group # can be given without the group # (or group 0) to produce commands for all groups.

# Notes
* You must first setup your WiFi bridge and sync/pair the light bulbs you want in each group.
* By default, there is a .025s wait between each command. This can be changed on init by setting the `wait_duration` parameter