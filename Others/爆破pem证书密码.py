# from Crypto.PublicKey import RSA
# import libnum
# import gmpy2
# with open("private.pem", "rb") as f:
#     key = RSA.import_key(f.read())
#     print("n = %d" % key.n)
#     print("e = %d" % key.e)
#     print("d = %d" % key.d)
#     print("p = %d" % key.p)
#     print("q = %d" % key.q)


# strs = "MTTC3TBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIVLQmLXnlUYkCAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBBCQKgOObf2BrhJ9tHvAb4oBIICgP3WaNdtO3oTAX1GjdqBL0f6HvFZ9q25EIOAah78rfhKNrJQP0uHHUnbIDKUZTSMwNZ7kNQAAnJPdjwhZVNbymCjUrVvqs0VD8GWncUlIIxrAkpsgqioABSKLoy280ubg2s1IV/sqbuuvN4ldPvnAvyrLLnNLgGyU86v2Q1ArFWfG4kgeZSpW06W6TwgeIZbjRSnLKFXx1VEhpZSCOadg/HOh8BfLbFlZiWgDiuTdVSzGq34fLV8jKYfUjhEffh/tCNhjU5E8M6ItqgXZYyjbBO2ujewBzV1JiBE0QvcavwT8JvV2IDQXBtQmBJZXH4Vqoo2n5YmUgUFDxoZSdAqOfh5kcgO0OgORhOrX/qNisaDfBMwGx2csywJBuSujzZ3ckV3Gv2ysMzRPKfyZ/v10zElsrKZHci2wDMZ4XYqNyvPDafWaxkSNXP64eYRS8J6WVgWycaPq0LkoJnuxtmOnlYlZ8cmY2zOf4WfyG7X+NhK6CllS0or2Y7fuqo80dmGTrg7cuVA1GguRMA6qZAOlbqu8zT53vGUOIHDRQFb8DUU5H6t+I3e0+0Qj8ZwgTtUMCx2/WLc0YAq18Al9okrtsxuYIQ815SSxXKOXZsX93hACLEFFkKOW7vNdBMJdVJnbPoaMotkDYtH/d8TYPrrtyOhPRa/Xl8BzA9J40Z3PE+5XaQfTC4Wx9GMb3y/Dv1lVXrAd9XvCPD8jr6tu+aQWpMAq0uLpF0kgyS/5FDfIpiEHMMuRQ+FBKS58HWVkX1yKNmXkljJRpwe53AHLuDgt+0LNhry+5ck2GFH7bkxU13WmotrtUtnSdIX7FZrQzbJmbwHiyMi7oGdKT7vxkr3aFY="
# for i in range(0,len(strs),64):
#     print(strs[i:i+64])

from Crypto.PublicKey import RSA

# 读取加密的私钥文件
file_in = open("private.pem", "rb")
encrypted_key = file_in.read()
file_in.close()

# 密码爆破函数
def passphrase_cracker():
    with open("pass.txt", "r", encoding="utf8") as file:
        passwords = file.readlines()

    # 尝试每个密码
    for password in passwords:
        passphrase = password.strip()
        try:
            key = RSA.import_key(encrypted_key, passphrase=passphrase)
            print(f"Passphrase cracked: {passphrase}")
            print("n = %d" % key.n)
            print("e = %d" % key.e)
            print("d = %d" % key.d)
            print("p = %d" % key.p)
            print("q = %d" % key.q)
            break
        except ValueError:
            continue


# 调用密码爆破函数
passphrase_cracker()