import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def Decrypt_AESinECB_mode(ciphertext: bytes,key: bytes):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext_padded, AES.block_size)
    return plaintext

if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"
    with open("7.txt", "r") as f:
        base64_str = "".join(line.strip() for line in f.readlines())
        aes_encrypted = base64.b64decode(base64_str)
        plaintext = Decrypt_AESinECB_mode(aes_encrypted,key)
        print(plaintext.decode())