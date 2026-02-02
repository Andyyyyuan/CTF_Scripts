from PIL import Image
img = Image.open('flag.png')
width, height = img.size
c_x = width // 2
c_y = height // 2

for count in range(3,width+1,2):
    print(count)
    d = count // 2
    for i in range((count-1)*4):
        p_x = c_x - d
        p_y = c_y - d
        tmp0 = img.getpixel((width//2,c_y-count//2))
        if(tmp0[0] == 255 and tmp0[1] == 255 and tmp0[2] == 255):
            break
        tmp = img.getpixel((p_x,p_y))
        for j in range(count-1):
            img.putpixel((p_x,p_y),(img.getpixel((p_x+1,p_y))))
            p_x += 1
        for j in range(count-1):
            img.putpixel((p_x,p_y),(img.getpixel((p_x,p_y+1))))
            p_y += 1
        for j in range(count-1):
            img.putpixel((p_x,p_y),(img.getpixel((p_x-1,p_y))))
            p_x -= 1
        for j in range(count-2):
            img.putpixel((p_x,p_y),(img.getpixel((p_x,p_y-1))))
            p_y -= 1
        img.putpixel((p_x,p_y),tmp)

img.save("trueflag.png")