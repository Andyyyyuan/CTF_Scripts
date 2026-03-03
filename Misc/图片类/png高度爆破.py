import binascii
import struct

def burpheight(data):
    for i in range(0xFFFF):
        stream = data[12:20] + struct.pack('>i', i) + data[24:32]
        crc32_value = binascii.crc32(stream).to_bytes(4, "big")
        if crc32_value == data[32:36]:
            print(f"Success! 图像高度为: {i} ({struct.pack('>i', i).hex()})")
            break
        
with open("xor_file", "rb") as f:
    data = f.read()
    
burpheight(data)