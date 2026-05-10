from Challenge7_Decrypt_AESinECB_mode import *

def decect_ECB_mode(ciphertext: bytes) -> int:
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    seen = set()
    duplicates = 0
    for block in blocks:
        if block in seen:
            duplicates += 1
        else:
            seen.add(block)
    return duplicates


if __name__ == "__main__":
    with open("8.txt", "r") as f:
        max_duplicate = -1
        max_duplicate_code = None
        for line in f.readlines():
            ciphertext = bytes.fromhex(line)
            current_duplicate = decect_ECB_mode(ciphertext)
            if current_duplicate > max_duplicate:
                max_duplicate = current_duplicate
                max_duplicate_code = line

        print("Possible ECB encrypted code:")
        print(max_duplicate_code)
