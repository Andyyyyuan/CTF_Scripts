def xor(data1, data2):

    """
    对两个字节、字符串或整数列表进行异或操作。
    输入要求：
    - data1 和 data2 必须是相同类型的可迭代对象（bytes、str、list等）
    - 若输入为字符串，将按默认编码（UTF-8）转为字节处理
    - 输入长度必须相同
    """

    if isinstance(data1, str):
        data1 = data1.encode()
    if isinstance(data2, str):
        data2 = data2.encode()

    if type(data1) != type(data2):
        raise TypeError("输入类型不一致（例如一个为字节，另一个为列表）")
    if len(data1) != len(data2):
        raise ValueError("输入长度不一致")

    if isinstance(data1, bytes):
        return bytes(a ^ b for a, b in zip(data1, data2))
    elif isinstance(data1, list):
        return [a ^ b for a, b in zip(data1, data2)]
    else:
        raise TypeError("仅支持 bytes、str 或整数列表类型")

if __name__ == '__main__': #https://cryptopals.com/sets/1/challenges/2
    data1 = "1c0111001f010100061a024b53535009181c"
    data2 = "686974207468652062756c6c277320657965"
    data1 = bytes.fromhex(data1)
    data2 = bytes.fromhex(data2)
    ans = xor(data1, data2)
    print(bytes.hex(ans))