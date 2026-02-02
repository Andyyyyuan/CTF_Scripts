import zlib
import binascii

# 从zlib.txt文件中读取内容
with open('zlib.txt', 'r') as f:
    content = f.read()

# 去掉空格和换行符
hex_data = content.replace(' ', '').replace('\n', '').replace('\r', '')

print(f"读取到的十六进制数据长度: {len(hex_data)} 字符")

# 将十六进制字符串转换为二进制数据
try:
    binary_data = binascii.unhexlify(hex_data)
    print(f"转换为二进制数据长度: {len(binary_data)} 字节")
    
    # 尝试解压缩数据
    decompressed_data = zlib.decompress(binary_data)
    print(f"解压缩后数据长度: {len(decompressed_data)} 字节")
    
    # 将解压缩后的结果写入新的txt文件
    with open('解压后的结果.txt', 'wb') as f:
        f.write(decompressed_data)
    
    print("解压缩成功，结果已保存到'解压后的结果.txt'文件中")
    print("\n解压缩后的数据前100个字节:")
    print(decompressed_data[:100])
    
except binascii.Error as e:
    print(f"十六进制转换错误: {e}")
except zlib.error as e:
    print(f"解压缩错误: {e}")
except Exception as e:
    print(f"发生其他错误: {e}")