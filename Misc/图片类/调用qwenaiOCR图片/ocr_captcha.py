import os
import re
import base64
import time
from config import *
import dashscope
from dashscope import MultiModalConversation

# 配置dashscope SDK
dashscope.api_key = API_KEY

def get_image_files(folder_path):
    """获取文件夹中所有按数字顺序命名的图片文件"""
    image_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # 提取文件名中的数字部分
            match = re.match(r"(\d+)\.(png|jpg|jpeg)$", filename)
            if match:
                image_files.append((int(match.group(1)), filename))
    
    # 按数字顺序排序
    image_files.sort(key=lambda x: x[0])
    return [os.path.join(folder_path, filename) for _, filename in image_files]

def encode_image_to_base64(image_path):
    """将图片编码为base64格式"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def call_qwen_api(image_path):
    """调用通义千问API进行OCR识别"""
    # 构造消息
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请识别图片中的4位数字验证码，仅返回数字，不要包含其他任何字符或解释。"
                },
                {
                    "type": "image",
                    "image": image_path  # 直接传入图像文件路径
                }
            ]
        }
    ]
    
    try:
        # 调用dashscope SDK
        response = MultiModalConversation.call(
            model="qwen-vl-plus",
            messages=messages,
            top_p=0.8,
            temperature=0.1
        )
        
        # 检查响应状态
        if response.status_code == 200 and "output" in response and "choices" in response["output"]:
            content = response["output"]["choices"][0]["message"]["content"]
            
            # 处理不同类型的content
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        # 检查是否有text键
                        if "text" in item:
                            return item["text"].strip()
                        # 尝试返回字典中的第一个字符串值
                        for value in item.values():
                            if isinstance(value, str):
                                return value.strip()
                    elif isinstance(item, str):
                        return item.strip()
                raise Exception(f"API返回内容中未找到文本: {content}")
            elif isinstance(content, str):
                return content.strip()
            elif isinstance(content, dict):
                # 检查是否有text键
                if "text" in content:
                    return content["text"].strip()
                # 尝试返回字典中的第一个字符串值
                for value in content.values():
                    if isinstance(value, str):
                        return value.strip()
                raise Exception(f"API返回内容中未找到文本: {content}")
            else:
                raise Exception(f"API返回内容格式未知: {type(content)} - {content}")
        else:
            raise Exception(f"API调用失败: {response}")
    
    except Exception as e:
        raise Exception(f"API调用失败: {str(e)}")

def clean_ocr_result(text):
    """清洗OCR识别结果，提取4位数字"""
    # 提取所有数字
    digits = re.findall(r"\d", text)
    
    # 检查是否有4位数字
    if len(digits) == 4:
        return "".join(digits)
    else:
        return None

def process_captcha(image_path):
    """处理单个验证码图片，包含重试机制"""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            ocr_result = call_qwen_api(image_path)
            cleaned_result = clean_ocr_result(ocr_result)
            
            if cleaned_result:
                return cleaned_result
            else:
                print(f"图片 {os.path.basename(image_path)} 识别结果不符合要求: '{ocr_result}'，正在重试 ({retries + 1}/{MAX_RETRIES})")
                retries += 1
                time.sleep(RETRY_DELAY)  # 重试间隔
        
        except Exception as e:
            print(f"图片 {os.path.basename(image_path)} 识别出错: {str(e)}，正在重试 ({retries + 1}/{MAX_RETRIES})")
            retries += 1
            time.sleep(RETRY_DELAY)  # 重试间隔
    
    return None

def main():
    """主函数"""
    folder_path = IMAGE_FOLDER
    image_files = get_image_files(folder_path)
    
    print(f"找到 {len(image_files)} 个图片文件")
    
    results = []
    errors = []
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"正在处理图片: {filename}")
        
        result = process_captcha(image_path)
        if result:
            results.append(result)
            print(f"识别结果: {result}")
        else:
            errors.append((filename, "超过最大重试次数"))
            print(f"图片 {filename} 识别失败，已跳过")
        
        # 避免请求过快
        time.sleep(REQUEST_DELAY)
    
    print("\n===== 识别完成 =====")
    print(f"成功识别: {len(results)} 个")
    print(f"识别失败: {len(errors)} 个")
    
    if errors:
        print("\n识别失败的图片:")
        for filename, error in errors:
            print(f"- {filename}: {error}")
    
    print("\n识别结果列表:")
    print(results)
    
    # 保存结果到文件
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(results))
    
    print("\n结果已保存到 ocr_results.txt")

if __name__ == "__main__":
    main()