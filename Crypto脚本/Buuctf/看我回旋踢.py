"""
rot13
"""
encrypted = "synt{5pq1004q-86n5-46q8-o720-oro5on0417r1}"
plaintext = ""

for c in encrypted:
    if 'a' <= c <= 'z':
        tmp = ord(c) - 13
        if tmp < ord('a'):
            tmp += ord('a')
        plaintext += chr(tmp)
    else:
        plaintext += c

print(plaintext)