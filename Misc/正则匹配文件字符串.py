import re

def find_pattern_in_binary_file(file_path):
    print(f"正在读取文件: {file_path}")

    try:
        with open(file_path, 'rb') as f:
            raw_bytes = f.read()

        content_str = raw_bytes.decode('latin-1')
        print(f"文件读取成功，长度: {len(content_str)}")
        
        pattern = r'\d[a-z]{5}[A-Z]{2}[^A-Z][A-Z](.)[a-z]\d{2}[A-Z]\D{5}'
        matches = re.findall(pattern, content_str)
        print(''.join(matches))

    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    target = r'E:\Admin\Desktop\第三届古剑山\hundred\workspace\flag99\enc.txt'
    
    find_pattern_in_binary_file(target)