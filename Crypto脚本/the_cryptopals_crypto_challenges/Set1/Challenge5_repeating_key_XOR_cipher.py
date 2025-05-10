def repeatingKeyXOR(plaintext, key):
    if isinstance(plaintext, bytes) and isinstance(key, bytes):
        encoded = b""
        for i,c in enumerate(plaintext):
            encoded += bytes([c ^ key[i % len(key)]])
        return encoded
    else:
        raise TypeError('plaintext and key must be of type bytes!')

if __name__ == '__main__':
    key = b"ICE"
    plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    print(repeatingKeyXOR(plaintext, key).hex())