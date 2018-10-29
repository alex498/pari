import dpath.util
from requests import get
import speech_recognition as sr
import vk,os,sys,subprocess,wave,contextlib,math,psutil
from time import *
import datetime
import urllib.request
from pydub import AudioSegment
length = 25

def pozdr(name):
    return '''$name, с днем рождения тебя!!!
Желаю тебе творческой реализации, пусть в твоей жизни всегда будет радость и счастье!'''.replace('$name',name)

def a_length(input_file):
    with contextlib.closing(wave.open(input_file,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return math.ceil(duration / length)

def cut_audio(input_file,num_pieces):       
    for i in range(num_pieces):
        output = 'output/'+input_file.replace('.','('+str(i)+').')
        if i==num_pieces-1:
            s = "ffmpeg -i "+input_file+" -ss "+str(i * length)+" -t "+str(a_length(input_file)%length)+" -acodec copy "+output
        else:
            s = "ffmpeg -i "+input_file+" -ss "+str(i * length)+" -t "+str(length)+" -acodec copy "+output
        print(s)
        subprocess.call(s,shell=True)
        for proc in psutil.process_iter():
        # check whether the process name matches
            if proc.name() == 'ffmpeg.exe':
                proc.kill()

def download(url, file_name, wavname):
    r = get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    sound = AudioSegment.from_mp3(file_name)
    sound.export(wavname, format="wav")

def links(msg):
    result = []
    ttemp = ''.join(msg)
    while 'link_mp3' in ttemp:
        start = ttemp.index("link_mp3")+12
        end = ttemp.index('.mp3')+4
        result.append(ttemp[start:end])
        ttemp = ttemp[end:]
    return result
        

group = '62884807'
login = '+79969127739'
password = '01qi1976'
vk_id = '6658198'
t1 = 'c02473bf25903bbb563e04e525a21556dfae97dc52702db07f196f1842977f944adeb0fdf3155226d07ed'
session = vk.AuthSession(access_token=t1)
vk_api = vk.API(session,v='5.82')

def write(ids,message):
    vk_api.messages.send(user_id=ids,message=message)
    sleep(1)

def respond_audio(link,ans_id,vk_api):
    name = link.split('/')[-1]
    wavname = name.split('.')[0]+'.wav'
    download(link,name,wavname)
    r = sr.Recognizer()
    parts = a_length(wavname)
    print(wavname,parts)
    if parts==1:        
        with sr.AudioFile(wavname) as source:
            audio = r.record(source)  # read the entire audio file
        try:
            text = "Я считаю, что сказали: " + r.recognize_google(audio, language="ru_RU")
            print(ans_id,text)
            vk_api.messages.send(user_id=ans_id, message=text)
            os.remove(name)
            os.remove(wavname)
        except:
            vk_api.messages.send(user_id=ans_id, message='Моя твоя не понимать')
            print(ans_id,'Моя твоя не понимать')
            os.remove(name)
            os.remove(wavname)
    else:
        text = "Я считаю, что сказали:"
        cut_audio(wavname,parts)
        for i in range(parts):
            with sr.AudioFile('output/'+wavname.replace('.','('+str(i)+').')) as source:
                audio = r.record(source)  # read the entire audio file
                try:
                    text += ' '+r.recognize_google(audio, language="ru_RU")
                    print(ans_id,text)
                except:
                    text='Моя твоя не понимать'
                    print(ans_id,'Моя твоя не понимать')
            os.remove('output/'+wavname.replace('.','('+str(i)+').'))
        os.remove(name)
        os.remove(wavname)
        vk_api.messages.send(user_id=ans_id, message=text)

a = True
while a:
    sleep(5)
    try:
        for msg in vk_api.messages.getDialogs(count=10, unread=1)['items']:
            if '!др' in str(msg['message']['body']):
                vk_api.messages.send(user_id=msg['message']['user_id'], message=pozdr(msg['message']['body'][3:]))
            if 'fwd_messages' in str(msg) and 'link_mp3' in str(msg):
                ans_id = msg['message']['user_id']
                for i in links(str(msg)):
                    respond_audio(i,ans_id,vk_api)
        
    except Exception as e:
        print(e,'restart')
        session = vk.AuthSession(access_token=t1)
        vk_api = vk.API(session, v='5.82')
      
        
    

    
