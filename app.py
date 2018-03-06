import vk
from time import *
import datetime
import urllib.request

days=['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
login = '+79969127739'
password = '01qi1976'
vk_id = '6397849'

def now_time():
    return datetime.datetime.utcnow()+datetime.timedelta(hours=4)

def nedelia():
    fp = urllib.request.urlopen("http://raspisanie.asu.edu.ru/")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    mystr=mystr.lower()
    if mystr.count('числитель')>mystr.count('знаменатель'):
        return '1'
    else:
        return '2'

def make_message():
    url = "http://raspisanie.asu.edu.ru/student/%D0%97%D0%9821/"+nedelia()
    urllib.request.urlopen(url).read()
    
    day=days[now_time().weekday()+1]
    url = "http://raspisanie.asu.edu.ru/student/%D0%97%D0%9821/"+nedelia()
    text = urllib.request.urlopen(url).read().decode('utf-8')
    if day!='Воскресенье':
        return 'Завтра к '+str(text[text.index(day)+len(day)+46:text.index(day)+len(day)+47])+' паре'
    else:
        return 'Завтра нет пар' 

session = vk.AuthSession(vk_id, login, password, scope='messages')
vk_api = vk.API(session, v='5.62')

while True:
    last_time=None
    if list(now_time().timetuple())[3]>22 and list(now_time().timetuple())[3]<24 and (last_time==None or ((now_time()-last_time).seconds // 3600)>22):
        print(vk_api.messages.send(user_id="95881708", message=make_message()))
        last_time=now_time()
    sleep(300)
        
        
    

    
