import time
import hashlib
import requests

current_time = str(time.time())
appid = 'wwdsafaewfdssadasasw'
m = hashlib.md5()
m.update(bytes(appid+current_time,encoding='utf-8'))
newappid = m.hexdigest()
new_newappid = '%s|%s'%(newappid,current_time)

response = requests.get('http://127.0.0.1:8000/post_info/',
                        # params={'appid':new_newappid})
                        headers={'appid':new_newappid})
print(response.text)