import struct
import zlib

def extract_idat_simple(png_file):
    with open(png_file, 'rb') as f:
        # 读取并验证PNG文件头
        header = f.read(8)
        idat_data = b''
        chunk_count = 0
        
        while True:
            try:
                # 读取块长度
                len_bytes = f.read(4)
                length = struct.unpack('>I', len_bytes)[0]
                # 读取块类型
                chunk_type = f.read(4)
                chunk_count += 1
                # 读取块数据
                data = f.read(length)
                # 跳过CRC
                f.read(4)
                
                # 处理IDAT块
                if chunk_type == b'IDAT':
                    idat_data += data
                    print(f"[+] 正在处理IDAT块{chunk_count}，长度: {length}")
                
                # 如果是IEND块，结束
                if chunk_type == b'IEND':
                    print(f"[+] 到达IEND块，IDAT块提取完毕，共提取 {chunk_count} 个块")
                    break
                    
            except struct.error:
                break
        
        return idat_data
            
if __name__ == "__main__":
    png_file = '？.png'
    data = extract_idat_simple(png_file)
    # print(len(data))
    # print(data.hex())
    decompressed_data = zlib.decompress(data)
    with open('extract_idat', 'wb') as f:
        f.write(decompressed_data)