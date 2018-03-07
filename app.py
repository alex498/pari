import vk
from time import *
import datetime
import urllib.request

p_start=['','8:30','10:10','11:50','13:40','15:20','16:55','18:30','20:05']
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

def make_message(mode):
    try:      
        url = "http://raspisanie.asu.edu.ru/student/%D0%97%D0%9821/"+nedelia()
        urllib.request.urlopen(url).read()
        if mode=='Сегодня':
            day=days[now_time().weekday()]
        if mode=='Завтра':
            day=days[now_time().weekday()+1]
        url = "http://raspisanie.asu.edu.ru/student/%D0%97%D0%9821/"+nedelia()
        text = urllib.request.urlopen(url).read().decode('utf-8')
        if day!='Воскресенье':
            para=str(text[text.index(day)+len(day)+46:text.index(day)+len(day)+47])
            return 'Завтра к '+p_start[int(para)]+' пара №'+para
        else:
            return  'Завтра нет пар'
    except:
        return 'Вероятно сайт расписания не работает сейчас'

session = vk.AuthSession(vk_id, login, password, scope='messages')
vk_api = vk.API(session, v='5.62')

l={'95881708':None,'147933155':None,'164138740':None}
d={'alex__brin':None,'ar4ibald98':None}

while True:
    for msg in vk_api.messages.get(count=10)['items']:
            if msg['read_state']==0: # get all unread messages
                if 'сегодня' in msg['body'].lower():
                    print(vk_api.messages.send(user_id=msg['user_id'], message=make_message('Сегодня')))
                if 'завтра' in msg['body'].lower():
                    print(vk_api.messages.send(user_id=msg['user_id'], message=make_message('Сегодня')))
                vk_api.messages.markAsRead(message_ids=msg['id'])
    for i in l:
        if list(now_time().timetuple())[3]>22 and list(now_time().timetuple())[3]<24 and (l[i]==None or ((now_time()-l[i]).seconds // 3600)>22):
            print(vk_api.messages.send(user_id=i, message=make_message('Завтра')))
            l[i]=now_time()
    for i in d:
        if list(now_time().timetuple())[3]>22 and list(now_time().timetuple())[3]<24 and (d[i]==None or ((now_time()-d[i]).seconds // 3600)>22):
            print(vk_api.messages.send(domain=i, message=make_message('Завтра')))
            d[i]=now_time()
    sleep(10)
        
        
    

    
