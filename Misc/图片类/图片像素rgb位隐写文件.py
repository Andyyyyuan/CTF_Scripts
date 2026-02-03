from PIL import Image

image = Image.open("lsb.png")
w,h = image.size

data = ""

for y in range(h):
    for x in range(w):
        r, g, b = image.getpixel((x,y))
        hexr, hexg, hexb = format(r, '02X'), format(g, '02X'), format(b, '02X')
        data += f"{hexg}{hexb}{hexr}"
        
print(data[:100])

bytedata = bytes.fromhex(data)

with open("ans.pcapng", "wb") as f:
    f.write(bytedata)
        