encrypted = "afZ_r9VYfScOeO_UL^RWUc"
plaintext = ""

j = 5
for i in encrypted:
    plaintext += chr(ord(i) + j)
    j += 1

print(plaintext)
