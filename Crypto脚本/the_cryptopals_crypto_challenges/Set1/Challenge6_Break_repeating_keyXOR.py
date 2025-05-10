import math
import base64
import statistics
from itertools import combinations

from Challenge5_repeating_key_XOR_cipher import *
from Challenge3_Singlebyte_XOR_cipher import *

def get_hamming_distance(a, b):
    if len(a) != len(b):
        raise "len(a) != len(b)"
    if isinstance(a, bytes) and isinstance(b, bytes):
        distance = 0
        for i,j in zip(a,b):
            xor = i ^ j
            distance += bin(xor).count("1")
        return distance
    else:
        raise "a,b must be bytes"

def GetKeyLength(str):
    best_key_size = -1
    min_normalized_distance = float("inf")

    for tmp_key_size in range(2,41):
        divided_num = len(str) // tmp_key_size
        idx_list = combinations(range(min(divided_num,5)), 2)
        #取块取的太少会导致密码长度不准确，取的太多速度会慢，这里我选择 range(min(divided_num,5))
        dist_list = []
        for idx in idx_list:
            pre = str[idx[0]*tmp_key_size:(idx[0]+1)*tmp_key_size]
            suf = str[idx[1]*tmp_key_size:(idx[1]+1)*tmp_key_size]
            tmp_hamming_distance = get_hamming_distance(pre, suf)
            tmp_normalized_distance = float(tmp_hamming_distance / tmp_key_size)

            dist_list.append(tmp_normalized_distance)

        #print(f"len={tmp_key_size}:{tmp_hamming_distance}:{tmp_normalized_distance}")

        average_normalized_distance = statistics.mean(dist_list)
        if average_normalized_distance < min_normalized_distance:
            min_normalized_distance = average_normalized_distance
            best_key_size = tmp_key_size
    return best_key_size

def transpose_blocks(stream: bytes, key_size: int) -> list[bytes]:
    block_list = [stream[shift::key_size] for shift in range(key_size)]
    return block_list

def single_XOR_decode(ciphertext):
    max_score = -float("inf")
    ans_key = None
    ans = None
    for key in range(256):
        decoded = bytes([b ^ key for b in ciphertext])
        tmp_score = score_plaintext(decoded)
        if tmp_score > max_score:
            ans_key = key
            max_score = tmp_score
            ans = decoded
    return ans,ans_key

def Decrypt_Repeating_XOR_Encoded(ciphertext: bytes):
    """
    频率分析+归一化距离解密xor循环加密
    :param ciphertext:xor循环加密的密文
    :return:
        plaintext:解密后的字符串,
        key_list:密钥
    """
    key_length = GetKeyLength(ciphertext)
    single_XOR_list = transpose_blocks(ciphertext, key_length)

    key_list = []
    decoded_list = []
    for block in single_XOR_list:
        single_decoded, single_key = single_XOR_decode(block)
        decoded_list.append(single_decoded)
        key_list.append(single_key)

    plaintext = repeatingKeyXOR(xor_encoded, bytes(key_list))

    return plaintext,key_list


if __name__ == "__main__":
    with open("6.txt", "r") as f:
        base64_str = "".join(line.strip() for line in f.readlines())
        xor_encoded = base64.b64decode(base64_str)
        Decrypt_Repeating_XOR_Encoded(xor_encoded)

        plaintext,key_list = Decrypt_Repeating_XOR_Encoded(xor_encoded)
        print("**********************************************")
        print("Decrypted Success!")
        print("**********************************************")
        print("Key: ", bytes(key_list).decode())
        print("**********************************************")
        print("Plaintext: \n", bytes(plaintext).decode())
