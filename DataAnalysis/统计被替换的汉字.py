import os
import re

def get_chinese_chars(text):
    """提取文本中的所有中文字符，并去重返回一个集合"""
    # 匹配中文字符的正则表达式
    pattern = re.compile(r'[\u4e00-\u9fff]')
    # 找到所有匹配的中文字符
    chinese_chars = pattern.findall(text)
    # 去重并返回集合
    return set(chinese_chars)

def compare_folders(folder1, folder2):
    """比较两个文件夹中的txt文件，找出中文字符被替换的情况"""
    replaced_chars = {}  # 存储被替换的字符，key为文件名，value为(原字符集, 新字符集)
    
    # 递归遍历文件夹1
    for root, dirs, files in os.walk(folder1):
        for file in files:
            # 只处理txt文件
            if file.endswith('.txt'):
                # 构建文件在两个文件夹中的完整路径
                file1_path = os.path.join(root, file)
                relative_path = os.path.relpath(file1_path, folder1)
                file2_path = os.path.join(folder2, relative_path)
                
                # 检查文件2是否存在
                if not os.path.exists(file2_path):
                    print(f"警告：文件 {file2_path} 不存在，跳过该文件")
                    continue
                
                # 读取文件内容
                try:
                    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
                        content1 = f1.read()
                        content2 = f2.read()
                except Exception as e:
                    print(f"错误：读取文件 {file1_path} 或 {file2_path} 时出错 - {str(e)}，跳过该文件")
                    continue
                
                # 提取中文字符并去重
                chars1 = get_chinese_chars(content1)
                chars2 = get_chinese_chars(content2)
                
                # 找出被替换的字符（只在一个文件中出现的字符）
                replaced = (chars1 - chars2) | (chars2 - chars1)
                
                if replaced:
                    replaced_chars[relative_path] = (chars1 - chars2, chars2 - chars1)
    
    return replaced_chars

def main():
    # 两个文件夹的路径
    folder1 = "E:\Admin\Desktop\G\爬取-原本"  # 替换为你的第一个文件夹路径
    folder2 = "E:\Admin\Desktop\G\爬取-替换"  # 替换为你的第二个文件夹路径
    
    # 检查文件夹是否存在
    if not os.path.isdir(folder1):
        print(f"错误：文件夹 {folder1} 不存在")
        return
    if not os.path.isdir(folder2):
        print(f"错误：文件夹 {folder2} 不存在")
        return
    
    # 比较文件夹中的txt文件
    replaced_chars = compare_folders(folder1, folder2)
    
    # 输出结果
    if replaced_chars:
        print("找到以下文件中的中文字符被替换：")
        print("=" * 50)
        for file, (removed, added) in replaced_chars.items():
            print(f"\n文件：{file}")
            if removed:
                print(f"  被移除的中文字符：{sorted(list(removed))}")
            if added:
                print(f"  新增的中文字符：{sorted(list(added))}")
        print("\n" + "=" * 50)
        print(f"总共有 {len(replaced_chars)} 个文件的中文字符被替换")
    else:
        print("两个文件夹中的txt文件中文字符完全一致，没有发现被替换的字符")

if __name__ == "__main__":
    main()