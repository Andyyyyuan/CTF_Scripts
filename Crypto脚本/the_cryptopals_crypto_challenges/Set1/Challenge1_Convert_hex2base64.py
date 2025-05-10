#https://cryptopals.com/sets/1/challenges/1
import base64

password = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

byte_data = bytes.fromhex(password) #把hex编码转换为字节串

base64_data = base64.b64encode(byte_data).decode('ascii')
#base64.b64encode()必须传入字节串，返回也是字节串，用.decode('ascii')转换成字符串

print(base64_data)
