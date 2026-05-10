from Challenge2_Fixed_XOR import xor

def score_plaintext(byte_str):
    """
    频率分析
    :param byte_str:必须为字节串
    :return:这个字节串的频率得分
    """
    english_freq = {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04258, 'e': 0.12702,
        'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
        'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
        'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
        'z': 0.00074, ' ': 0.13000, ',': 0.012, '.': 0.010, "'": 0.001, '!': 0.001
    }

    score = 0.0
    for byte in byte_str:
        char = chr(byte).lower()
        if char in english_freq:
            score += english_freq[char]
        elif 32 <= byte <= 126:
            score += 0.0
        else:
            score -= 0.1
    return score

if __name__ == '__main__':#https://cryptopals.com/sets/1/challenges/3
    encoded = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    encoded = bytes.fromhex(encoded)
    print(encoded)

    best_score = -float('inf')
    best_key = None
    ans = None
    for key in range(256):
        decoded = bytes([b ^ key for b in encoded])
        current_score = score_plaintext(decoded)
        if current_score > best_score:
            best_score = current_score
            best_key = key
            ans = decoded

    print(f"the answer is: {ans.decode('ascii')}")
    print(f"the key is: {chr(best_key)}")
    print("the best score is: %.4f"%best_score)
