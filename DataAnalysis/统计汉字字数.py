import os
import re

def count_chinese_chars(file_path):
    """统计单个文件中的中文字符数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            # 使用正则匹配中文字符
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
            return len(chinese_chars)
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return 0

def count_chinese_in_folder(folder_path):
    """递归统计文件夹下所有txt文件的中文字符数"""
    total_chars = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                char_count = count_chinese_chars(file_path)
                total_chars += char_count
                print(f"{file_path}: {char_count} 个中文字符")
    print(f"\n总中文字符数: {total_chars} 个")

if __name__ == "__main__":
    folder = input("请输入文件夹路径: ")
    count_chinese_in_folder(folder)
