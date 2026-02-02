from PIL import Image

file_path = "attachment.png"

image = Image.open(file_path).convert("RGBA")
width, height = image.size

print(width,height)

spot_width = []
spot_height = []

for h in range(height):
    r, g, b, a = image.getpixel((24, h))
    if r == 255 and g == 255 and b == 255:
        spot_width.append(h)
        
for w in range(width):
    r, g, b, a = image.getpixel((w, 2189))
    if r == 255 and g == 255 and b == 255:
        spot_height.append(w)

ans_width = len(spot_width)
ans_height = len(spot_height)

image_ans = Image.new("RGB",(ans_width,ans_height))

for i, h in enumerate(spot_height):
    for j, w in enumerate(spot_width):
        r, g, b, a = image.getpixel((h, w))
        image_ans.putpixel((j,i), (r,g,b))

image_ans = image_ans.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
image_ans.save('gradient_image.jpg')
