import zlib
import struct
import argparse
import itertools

def calculate_bpp(bit_depth, color_type):
    """根据位深度和颜色类型计算每像素字节数"""
    if color_type == 0:  # 灰度
        return bit_depth // 8
    elif color_type == 2:  # RGB
        return (bit_depth * 3) // 8
    elif color_type == 3:  # 索引色
        return bit_depth // 8
    elif color_type == 4:  # 带Alpha的灰度
        return (bit_depth * 2) // 8
    elif color_type == 6:  # 带Alpha的RGB
        return (bit_depth * 4) // 8
    else:
        raise ValueError(f"不支持的颜色类型: {color_type}")


def extract_idat_data(bin_data):
    """提取所有IDAT块的数据并拼接"""
    idat_data = b''
    offset = 8  # 跳过PNG签名
    
    while offset < len(bin_data):
        # 读取块长度和类型
        length = struct.unpack('>I', bin_data[offset:offset+4])[0]
        chunk_type = bin_data[offset+4:offset+8]
        chunk_data = bin_data[offset+8:offset+8+length]
        
        if chunk_type == b'IDAT':
            idat_data += chunk_data
        elif chunk_type == b'IEND':
            break
            
        # 跳过当前块（长度+类型+数据+CRC）
        offset += 4 + 4 + length + 4
    
    return idat_data


def 爆破宽高未知CRC(bin_data):
    """在CRC未知情况下通过分析IDAT数据爆破宽高"""
    # 解析IHDR块获取位深度和颜色类型
    bit_depth = bin_data[24]
    color_type = bin_data[25]
    bpp = calculate_bpp(bit_depth, color_type)
    
    # 提取IDAT数据
    idat_data = extract_idat_data(bin_data)
    if not idat_data:
        print("未找到IDAT块数据")
        return
    
    print(f"位深度: {bit_depth}, 颜色类型: {color_type}, 每像素字节数: {bpp}")
    print("开始爆破宽高...")
    
    # 估算合理的宽高范围
    # 根据IDAT数据大小估算，假设压缩率在10-100%之间
    max_possible_size = len(idat_data) * 10
    max_dimension = min(8192, max_possible_size // (bpp + 1))  # 假设最小高度为1
    
    try:
        # 先解压缩IDAT数据，避免重复解压缩
        decompressed = zlib.decompress(idat_data)
        decompressed_size = len(decompressed)
        print(f"解压缩成功，数据大小: {decompressed_size} 字节")
        
        # 遍历可能的宽高组合，寻找符合条件的尺寸
        for height in range(1, max_dimension + 1):
            # 计算每行的字节数（包括过滤类型字节）
            # expected_size = height * (width * bpp + 1)
            # 所以 width = (expected_size / height - 1) / bpp
            # 因此，height必须是(decompressed_size)的因数，且满足以下条件
            if decompressed_size % height != 0:
                continue
            
            row_size = decompressed_size // height
            if row_size < 1:  # 每行至少需要1个字节（过滤类型字节）
                continue
            
            # 计算宽度
            if (row_size - 1) % bpp != 0:
                continue
            
            width = (row_size - 1) // bpp
            if width < 1 or width > max_dimension:
                continue
            
            # 检查所有扫描行的过滤类型是否有效（0-4）
            valid = True
            for i in range(height):
                filter_type = decompressed[i * row_size]
                if filter_type < 0 or filter_type > 4:
                    valid = False
                    break
            
            if valid:
                print(f"\n找到可能的宽高组合:")
                print(f"宽度: {width}, 高度: {height}")
                print(f"解压缩数据大小: {decompressed_size}, 每行大小: {row_size} 字节")
                print(f"每行像素数据: {row_size - 1} 字节")
                # 可以继续寻找更多可能的组合，或者返回第一个找到的
                # return width, height
    
    except zlib.error as e:
        print(f"解压缩失败: {e}")
        return
    
    print("未找到匹配的宽高组合")


def 爆破宽高已知CRC(bin_data):
    """原有的CRC已知情况下的宽高爆破方法"""
    crc32key = zlib.crc32(bin_data[12:29])  # 计算当前宽高的crc
    original_crc32 = int(bin_data[29:33].hex(), 16)  # 原始crc
    
    if crc32key == original_crc32:  # 计算crc对比原始crc
        print('宽高没有问题!')
    else:
        input_ = input("宽高被改了, 是否使用CRC爆破宽高? (Y/n):")
        if input_ not in ["Y", "y", ""]:
            return
        
        print("开始CRC爆破宽高...")
        for i, j in itertools.product(range(4095), range(4095)):  # 限制范围以提高速度
            data = bin_data[12:16] + struct.pack('>i', i) + struct.pack('>i', j) + bin_data[24:29]
            crc32 = zlib.crc32(data)
            if crc32 == original_crc32:
                print(f"\nCRC32: {hex(original_crc32)}")
                print(f"宽度: {i}, hex: {hex(i)}")
                print(f"高度: {j}, hex: {hex(j)}")
                return
        
        print("未找到匹配的宽高组合")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="输入图片文件路径")
    parser.add_argument("--unknown-crc", action="store_true", help="使用CRC未知的宽高爆破模式")
    args = parser.parse_args()
    
    try:
        bin_data = open(args.f, 'rb').read()
        
        # 验证PNG文件
        if bin_data[:8] != b'\x89PNG\r\n\x1a\n':
            print("不是有效的PNG文件")
            exit(1)
        
        if args.unknown_crc:
            爆破宽高未知CRC(bin_data)
        else:
            爆破宽高已知CRC(bin_data)
            
    except FileNotFoundError:
        print(f"文件不存在: {args.f}")
    except Exception as e:
        print(f"发生错误: {str(e)}")
