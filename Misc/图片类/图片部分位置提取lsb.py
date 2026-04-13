from PIL import Image


def extract_lsb(image_path, start_x, start_y, end_x, end_y):

    img = Image.open(image_path)
    pixels = img.load()
    
    binary_data = ""
    
    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
    
            pixel = pixels[x, y]
    
            if len(pixel) == 4:
                r, g, b, _ = pixel 
            else:
                r, g, b = pixel 
    
            binary_data += bin(r)[-1]  # Red channel LSB
            binary_data += bin(g)[-1]  # Green channel LSB
            binary_data += bin(b)[-1]  # Blue channel LSB
    
    hidden_data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        hidden_data += chr(int(byte, 2))
    
    return hidden_data

image_path = "decrypted_image.png"
start_x, start_y = 1243, 1243
end_x, end_y = 1257,1254
hidden_message = extract_lsb(image_path, start_x, start_y, end_x, end_y)

print("Hidden Message:", hidden_message)
