def half2full(half):
    full = ''
    for ch in half:
        if ord(ch) in range(33, 127):
            ch = chr(ord(ch) + 0xfee0)
        elif ord(ch) == 32:
            ch = chr(0x3000)
        else:
            pass
        full += ch
    return full


while 1:
    t = ''
    s = input("输入想要转换的数字字符串：")
    for i in s:
        t += half2full(i)
    print(t)
