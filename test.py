import milight.white

light = milight.MiLight('192.168.0.12')

light.send(milight.rgbw.ON[1])
light.send(milight.rgbw.color_from_rgb(0xff, 0x00, 0x00, 1))
light.send(milight.rgbw.brightness(0, 1))
light.send(milight.rgbw.fade_up(1))

light.send(milight.rgbw.fade_down(1))

light.send(milight.rgbw.OFF[1])

#light.send(milight.white.party_mode('random', 1))


"""

c = colorsys.rgb_to_hls(1, 0, 0)
b = int(math.floor(c[0] * 255))

colors = []
colors.append(("Violet",0x00,"#EE82EE"))
colors.append(("RoyalBlue",0x10,"#4169E1"))
colors.append(("LightSkyBlue", 0x20,"#87CEFA"))
colors.append(("Aqua",0x30,"#00FFFF"))
colors.append(("AquaMarine", 0x40,"#7FFFD4"))
colors.append(("SeaGreen",0x50,"#2E8B57"))
colors.append(("Green",0x60,"#008000"))
colors.append(("LimeGreen",0x70,"#32CD32"))
colors.append(("Yellow",0x80,"#FFFF00"))
colors.append(("Goldenrod",0x90,"#DAA520"))
colors.append(("Orange",0xA0,"#FFA500"))
colors.append(("Red",0xB0,"#FF0000"))
colors.append(("Pink",0xC0,"#FFC0CB"))
colors.append(("Fuchsia", 0xD0,"#FF00FF"))
colors.append(("Orchid",0xE0,"#DA70D6"))
colors.append(("Lavender",0xF0,"#E6E6FA"))

for clover in colors:
    calc = milight.rgb_to_8bit(*milight.hex_to_rgb(clover[2]))
    light.send(milight.Command(0x40, calc))
    print('Color: %s, test %d, calc\'d %d' % (clover[0], clover[1], calc))
    time.sleep(2)

#print('Color: ', b)
#light.send(milight.Command(0x40, b))



#for i in range(0,256):
#    light.send(milight.Command(0x40, i))
"""
    
