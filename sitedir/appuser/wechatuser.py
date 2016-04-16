import pycurl
import json
import os
from .models import DirPersonnel

def getCatch(url, filename):
    fp = open(filename, "wb")
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.TIMEOUT, 300)
    curl.setopt(pycurl.NOSIGNAL, 1)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.setopt(pycurl.HEADER, False)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    try:
        curl.perform()
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
    curl.close()
    fp.close()

def getCode(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return(data)
    
def saveinfo(data):
    try:
        person = DirPersonnel.objects.get(openid=data['openid'])
    except DirPersonnel.DoesNotExist:
        person = DirPersonnel(openid=data['openid'], user_name=data['nickname'], gender=data['sex'], first_name='', last_name='', city=['city'], province_state=data['province'], country=['country'])
        person.save()

def getUser(request):
    wechatcode = request.GET.get('code', 'unknown')
    data1 = "data"
    appsecret = getCode('../etc/appsecret.json')
    AppID = appsecret['AppID']
    AppSecret = appsecret['AppSecret']
    Code = wechatcode
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + AppID + "&secret=" + AppSecret + "&code=" + Code + "&grant_type=authorization_code"
    getCatch(url, data1)    
    datadict1 = getCode(data1)
    url2 = "https://api.weixin.qq.com/sns/userinfo?access_token=" + datadict1['access_token'] + "&openid=" + datadict1['openid']
    data2 = "data2"
    getCatch(url2, data2)
    datadict = getCode(data2)
    saveinfo(datadict)
    os.remove(data1)
    os.remove(data2)
    return datadict
    