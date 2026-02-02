import string

# 标准英文各字母的出现频率 (基于大量文本统计)
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def clean_text(text):
    """只保留大写字母，去除标点和空格"""
    return "".join([c.upper() for c in text if c.isalpha()])

def get_index_of_coincidence(text):
    """
    计算重合指数 (Index of Coincidence)
    英文文本的IC通常接近 0.065，随机文本接近 0.038
    """
    N = len(text)
    if N < 2: return 0
    freqs = {c: text.count(c) for c in string.ascii_uppercase}
    numerator = sum(n * (n - 1) for n in freqs.values())
    return numerator / (N * (N - 1))

def guess_key_length(ciphertext, max_len=20):
    """
    通过比较IC值来猜测密钥长度
    返回最可能的密钥长度列表 (长度, 平均IC值)
    """
    candidates = []
    
    for length in range(1, max_len + 1):
        # 将密文切分成 length 个列
        columns = [''] * length
        for i, char in enumerate(ciphertext):
            columns[i % length] += char
        
        # 计算每一列的IC平均值
        avg_ic = sum(get_index_of_coincidence(col) for col in columns) / length
        
        # 英文IC 标准约为 0.065
        diff = abs(avg_ic - 0.065) 
        candidates.append((length, avg_ic, diff))
    
    # 按接近0.065的程度排序
    candidates.sort(key=lambda x: x[2])
    return candidates

def chi_squared_score(text):
    """
    计算文本频率与标准英文频率的卡方统计量。
    值越小，说明越像英文。
    """
    length = len(text)
    if length == 0: return float('inf')
    
    counts = {c: text.count(c) for c in string.ascii_uppercase}
    score = 0.0
    
    for char in string.ascii_uppercase:
        observed = counts[char]
        expected = length * ENGLISH_FREQ[char]
        score += ((observed - expected) ** 2) / expected
        
    return score

def decrypt_caesar(text, shift):
    """解密凯撒密码片段"""
    result = []
    for char in text:
        # (char_code - shift) mod 26
        decoded = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        result.append(decoded)
    return "".join(result)

def crack_key(ciphertext, key_len):
    """给定密钥长度，通过词频攻击找出具体密钥"""
    key = ""
    # 将密文分为 key_len 个组
    columns = [''] * key_len
    for i, char in enumerate(ciphertext):
        columns[i % key_len] += char
        
    for col in columns:
        best_shift = 0
        min_chi_sq = float('inf')
        
        # 尝试 a-z 26种位移
        for shift in range(26):
            decrypted_col = decrypt_caesar(col, shift)
            score = chi_squared_score(decrypted_col)
            
            if score < min_chi_sq:
                min_chi_sq = score
                best_shift = shift
        
        key += chr(best_shift + ord('A'))
        
    return key

def vigenere_decrypt(ciphertext, key):
    """使用得到的密钥解密完整文本"""
    # 原始文本可能包含空格标点，这里为了演示只处理了清理后的版本
    # 如果需要保留格式，需修改这里的逻辑
    plaintext = []
    key_idx = 0
    key = key.upper()
    
    for char in ciphertext:
        shift = ord(key[key_idx % len(key)]) - ord('A')
        decoded = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        plaintext.append(decoded)
        key_idx += 1
    return "".join(plaintext)

# ================= 使用示例 =================

def main():
    print("=== 维吉尼亚无密钥解密工具 ===")
    
    # 示例密文 (明文: "ATTACKATDAWN", Key: "LEMON")
    # 加密后应为: LXFOPVEFRNHR 
    # 为了演示效果，这里使用一段较长的密文，否则频率分析不准确
    # 这是一个使用密钥 "CRYPTO" 加密的英文段落
    raw_ciphertext = ""
    raw_ciphertext = input("请输入密文: ").strip()

    # 1. 清理文本
    clean_cipher = clean_text(raw_ciphertext)
    
    if len(clean_cipher) < 20: 
        print("\n警告: 密文过短，频率攻击可能失败！")

    # 2. 猜测密钥长度
    print("\n[-] 正在根据重合指数(I.C.)分析密钥长度...")
    candidates = guess_key_length(clean_cipher)
    
    # 打印前3个最可能的长度
    print(f"    最可能的长度是: {candidates[0][0]} (IC={candidates[0][1]:.4f})")
    print(f"    备选长度: {candidates[1][0]}, {candidates[2][0]}")
    
    # 默认取最可能的长度
    best_len = candidates[0][0]
    
    # 3. 破解密钥
    print(f"\n[-] 正在基于长度 {best_len} 进行卡方检验破解密钥...")
    guessed_key = crack_key(clean_cipher, best_len)
    print(f"    >>> 破解出的密钥: {guessed_key}")
    
    # 4. 解密
    plaintext = vigenere_decrypt(clean_cipher, guessed_key)
    print("\n[-] 解密结果 (前200字符):")
    print("-" * 40)
    print(plaintext[:200])
    print("-" * 40)

if __name__ == "__main__":
    main()