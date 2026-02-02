from scipy.io import wavfile
import numpy as np
from PIL import Image

sample_rate, data = wavfile.read("flag.wav")
img = Image.new('RGBA', (1021,761))

#print(data)

for y in range(761):
    for x in range(1021):
        pos = (x + y * 1021) * 5
        LeftVal = data[pos][0]
        RightVal = data[pos][1]
        r, g = (LeftVal >> 8) & 0xFF, LeftVal & 0xFF
        b, a = (RightVal >> 8) & 0xFF, RightVal & 0xFF
        r, g, b, a = int(r), int(g), int(b), int(a)
        img.putpixel((x,y), (r,g,b,a))
    
img.save("res.png")