import urllib.request
import re 
import http.cookiejar
from bs4 import BeautifulSoup
from pylogin.des import *
import json

from pylogin.captchaDeal import getCaptcha


    
class KINGGOFT:
    
    def __init__(self,username='15020021016',password='KL5864300'):
        
        
       
        
        
        self.username = username
        self.password = password
        self.indexUrl = 'http://jwgl.ouc.edu.cn/cas/login.action'
        self.logonUrl = 'http://jwgl.ouc.edu.cn/cas/logon.action'
        self.head = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'}
        cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
        
        
        
#***************************************登陆**********************************************************#
    def login(self):
        

        #获取 _sessionid
        def getSessionid():
            
            response = self.opener.open(self.indexUrl)
            html = response.read()
            soup = BeautifulSoup(html,'lxml')
            originalStr = soup.head.find(text=re.compile('.kingo')) #得到原始字符串    
            sessionid =re.findall('"([^"]+)"',originalStr)[1]  #对字符串进行处理得到需要的_sessionid
            return sessionid
        
        #获取验证码的值    
        def getRandnumber():
            
            imgUrl = 'http://jwgl.ouc.edu.cn/cas/genValidateCode'
            imgresponse = self.opener.open(imgUrl)
            image = imgresponse.read()
            filename = 'ouc_img.jpg'
            with open(filename,'wb') as jpg:
                jpg.write(image)
                jpg.close()
        
            randnumber = getCaptcha(filename)
            print('获取验证码成功!验证码为: ',randnumber)
            return randnumber
        
        #获取_nowtime 和 _deskey
        def getKeys():
                                        
            keyUrl = 'http://jwgl.ouc.edu.cn:80/custom/js/SetKingoEncypt.jsp'
            keyResponse = self.opener.open(keyUrl)
            key_html = keyResponse.read()
            soup_key = BeautifulSoup(key_html,'lxml')
            keylist =re.findall("'(.*)'",soup_key.text)
            return keylist
        
        #对服务器进行请求
        def post(randnumber,timestamp,_deskey):

            passwordPolicy = '1'
            password = md5(md5(self.password)+md5(randnumber.lower()))
            username = base64(self.username+";;"+_sessionid)
            p_username = "_u"+randnumber
            p_password = "_p"+randnumber
            params = p_username+"="+username+"&"+p_password+"="+password+"&randnumber="+randnumber+"&isPasswordPolicy="+passwordPolicy
      
            
       
            data = getEncParams(params,timestamp,_deskey)
            req = urllib.request.Request(self.logonUrl,data,self.head)
            response1 = self.opener.open(req)
        
            return response1
        
        #获取状态吗
        def getStatus():
            
            randnumber = getRandnumber()       
            
            keylist = getKeys()
            _deskey = keylist[0]
            timestamp = keylist[1]
            response1 = post(randnumber,timestamp,_deskey)
            #登陆结果验证
            result = response1.read().decode()
            result = json.loads(result)
            message = result['message']
            print('登陆的结果是: ',message)

            return result['status']
        
        _sessionid = getSessionid()

        #获取状态码,若登陆失败则重新登陆
        for times in range(3):
            status = getStatus()
            if status == '200':
                break

    def getScores(self):
    
        def getKeys():
                                        
            keyUrl = 'http://jwgl.ouc.edu.cn:80/custom/js/SetKingoEncypt.jsp'
            keyResponse = self.opener.open(keyUrl)
            key_html = keyResponse.read()
            soup_key = BeautifulSoup(key_html,'lxml')
            keylist =re.findall("'(.*)'",soup_key.text)
            return keylist
    
    
    
        
        url_scores='http://jwgl.ouc.edu.cn/student/xscj.stuckcj_data.jsp'
        params='xn=2016&xn1=1&xq=1&ysyx=yscj&sjxz=sjxz3&userCode='+'16070001041'
    
        self.head['Referer']='http://jwgl.ouc.edu.cn/oucjw/student/xscj.stuckcj.jsp?menucode=JW130705'

    #加密查询字段
        keylist = getKeys()
        _deskey = keylist[0]
        timestamp = keylist[1]
        dic=getEncParams(params,timestamp,_deskey)
        
    #获取查询结果
        req=urllib.request.Request(url_scores,dic,headers=self.head)
        
        response = self.opener.open(req)
        html=response.read()
        soup=BeautifulSoup(html,'lxml')
                             
        try:
            for tr in soup.find_all('tr'):
                for string in tr.stripped_strings:
                    print(string,end=' ')
                print('\n')
        except AttributeError:
        #print(soup.prettify())
            print('未查询到结果')
        #break

if __name__ =='__main__':
    spider = KINGGOFT()
    spider.login()
    spider.getScores()