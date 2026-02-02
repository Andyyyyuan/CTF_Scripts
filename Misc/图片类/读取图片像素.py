from PIL import Image
img = Image.open("file.png").convert("RGB")
w,h = img.size

for i in range(0,h,10):
    line = ""
    for j in range(0,w,10):
        pixel = img.getpixel((j,i))
        if pixel[2] == 254:
            line += "1"
        else:
            line += "0"
    print(chr(int(line,2)),end = "")
    