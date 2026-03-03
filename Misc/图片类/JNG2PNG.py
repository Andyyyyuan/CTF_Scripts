import binascii
import struct
import zlib
from PIL import Image

def jng2png(data):
    zlib_data = data.split(b"IDAT")[1].split(b"\x4A\x44\x41\x54")[0]
    zlib_data = zlib_data[:-8]
    alpha_data = zlib.decompress(zlib_data)
    
    jpg = Image.open("1.jpg")
    img1 = Image.new("RGBA", jpg.size)
    img2 = Image.new("L", jpg.size)
    
    for y in range(jpg.size[1]):
        for x in range(jpg.size[0]):
            alpha = (alpha_data[1 + y * 129 + x // 8] >> (7 - x % 8) & 1) * 255
            img1.putpixel((x,y), tuple(list(jpg.getpixel((x,y))) + [alpha]))
            img2.putpixel((x,y), 255) if alpha == 255 else img2.putpixel((x,y), 0)
    
    img1.save('combine.png')
    img2.save('alpha_mask.png')
    
with open("xor_file_repair", "rb") as f:
    data = f.read()
    
jng2png(data)