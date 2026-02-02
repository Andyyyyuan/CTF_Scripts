# -*- coding: utf-8 -*-
# 脚本编写：XSimple AI Assistant（修正版）

import os
import zipfile
import shutil
import sys
import re

def reverse_bytes(src_path, dst_path):
    """
    读取源文件，将所有字节完全倒序，保存到目标路径。
    """
    try:
        with open(src_path, 'rb') as f:
            content = f.read()

        reversed_content = content[::-1]

        with open(dst_path, 'wb') as f:
            f.write(reversed_content)
        return True
    except Exception as e:
        print(f"[!] 倒序转换失败: {e}")
        return False


def solve_puzzle(initial_file):
    current_input = initial_file

    # 从文件名中自动推断当前 flag 序号，例如 flag2 -> 2
    base = os.path.basename(initial_file)
    m = re.match(r"flag(\d+)", base)
    if m:
        current_index = int(m.group(1))
    else:
        current_index = 1  # 找不到就从 1 开始

    work_dir = "workspace"
    # 清理旧环境
    if os.path.exists(work_dir):
        try:
            shutil.rmtree(work_dir)
        except Exception as e:
            print(f"[!] 清理旧 workspace 失败: {e}")

    os.makedirs(work_dir, exist_ok=True)

    # 复制初始文件
    current_path = os.path.join(work_dir, os.path.basename(current_input))
    shutil.copy(current_input, current_path)

    print(f"[*] 开始处理，初始文件: {current_input}")

    while True:
        # 定义生成的 zip 路径
        zip_path = current_path + ".zip"

        # 1. 倒序生成 ZIP
        if not reverse_bytes(current_path, zip_path):
            print("[-] 无法继续倒序，脚本结束。")
            break

        # 2. 判断是否到达终点（倒序后已不是 ZIP 了）
        if not zipfile.is_zipfile(zip_path):
            print(f"\n[-] 文件倒序后已不再是 ZIP 格式。")
            print("[-] 可能已到达最后一层。")

            final_txt = "final_flag.txt"
            try:
                shutil.copy(zip_path, final_txt)
                print(f"[SUCCESS] 最终结果已保存为: {final_txt}")
                try:
                    with open(final_txt, 'r', errors='ignore') as f:
                        preview = f.read(200)
                        print(f"[*] 内容预览(前 200 字符):\n{preview}")
                except Exception as e:
                    print(f"[!] 预览内容失败: {e}")
            except Exception as e:
                print(f"[!] 保存最终结果失败: {e}")

            # 清理临时 zip
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except:
                pass
            break

        # 3. 解压逻辑
        extract_success = False
        found_file = ""

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_list = zf.namelist()

                if not file_list:
                    print("[-] 压缩包为空。")
                    break

                # 期望下一层文件名：flag{current_index+1}
                expected_name = f"flag{current_index + 1}"

                if expected_name in file_list:
                    file_to_extract = expected_name
                else:
                    # 容错：不存在就取第一个
                    file_to_extract = file_list[0]

                zf.extract(file_to_extract, work_dir)
                extract_success = True
                found_file = file_to_extract
                print(f"[+] ({current_index} -> {current_index + 1}) 解压提取: {file_to_extract}")

        except Exception as e:
            print(f"[-] 解压出错: {e}")
            break

        # 清理上一层的原始文件和 zip
        try:
            if os.path.exists(current_path):
                os.remove(current_path)
        except:
            pass

       

        if extract_success:
            # 指针前移
            current_path = os.path.join(work_dir, found_file)
            current_index += 1
        else:
            print("[-] 未能成功提取文件，脚本结束。")
            break


if __name__ == '__main__':
    # 修改这里为你的初始文件名，例如 "flag2"
    source_file = "flag2"

    if os.path.exists(source_file):
        solve_puzzle(source_file)
    else:
        print(f"错误：找不到文件 {source_file}")
