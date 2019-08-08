# coding:utf-8

from hashlib import md5,sha1
from hmac import HMAC
from urllib.parse import urlsplit,urljoin,quote,unquote,parse_qsl 
from collections import OrderedDict
import json
import logging
import re
from pathlib import Path
import os
from time import time
from random import choice
import json
import functools
import datetime
from requests.exceptions import ProxyError
from requests import Session
from threading import Thread,Event
from http.cookies import SimpleCookie
from base64 import b64decode , b64encode
import rsa


class Base(Session):
    '''客户端工具类的基类：
        功能：淘宝h5md5加密
            淘宝hmac加密，暂时未知真实加密步骤
            生成URL对象
            生成requests参数对象
    '''

    def __init__(self):
        # self.req_config = OrderedDict({
        #     'method':'',
        #     'domain':'',
        #     'path'
        # })
        super(Base,self).__init__()
        # self.console()
        self.stop_event = Event()
        self.loggerManager = {}
        self.headers.update({
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        })
        # self.log = False
        # self.log_format = ''
        self.um_payload = {"xv":"3.3.7","xt":"H5PWD79aa8f9c1ff38062b628f0d6e571f829","etf":"b","xa":"0000000000000A2126231E1B","siteId":"","uid":"","eml":"AA","etid":"","esid":"","type":"pc","nce":True,"plat":"Win32","nacn":"Mozilla","nan":"Netscape","nlg":"zh-CN","sw":400,"sh":700,"saw":400,"sah":700,"bsw":400,"bsh":700,"eloc":"https%3A%2F%2Fauth.alipay.com%2Flogin%2Fh5Login.htm","etz":480,"ett":1564796746956,"ecn":"b1877374a585615bcfe674df2ed01deaa8c7a1c5","erd":"default,communications,8255636708cdb825d4d6ec28f943f32c3bec6aabffd9ebbbe297ce35ad476ae7,f72a39248d9058f2c328f35ac10a0c7f3a0a5c3a1d897196e6bff8b070488bce,default,communications,e9124033a0785121a6d0554b64dfde8e68570506e1f276fd49c4c522eec35c72","ips":"192.168.10.101","epl":0,"ep":"da39a3ee5e6b4b0d3255bfef95601890afd80709","epls":"","esl":False}

    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    # def __getattr__(self,name):
    #     '''属性访问器，当通过这个来访问的时候，判断
    #     有没有mtop属性，有的时候返回taobao对象的方法
    #     改用公共对象的方法访问，用于以后扩展需要
    #     '''
    #     #判断公共对象是否有这个属性，没有则报错
    #     if self.__public__:
    #         obj = list(filter(lambda obj:hasattr(obj,name),self.__public__))
    #         if obj:
    #             return obj[0][name]
    #         else:
    #             raise AttributeError
    #     else:
    #         raise AttributeError
    
    # def __getattribute__(self,name):
    #     '''属性访问监听器
    #     如果有添加监听器并且匹配到，将把值传入匹配的回调函数中
    #     '''
    #     val = object.__getattribute__(self,name)
    #     # if self.loggerManager.get(name) and isinstance(self.loggerManager.get(name),list):
    #     #     for func in self.loggerManager.get(name):
    #     #         val = func(val)
        
    #     return val
    
    def getUmidToken(self):
        '''获取umidToken'''
        return 'C' + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(11)) + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(3))
    
    def getCookie(self,name:str="_m_h5_tk",domain:str='.taobao.com',start:int=0,end:int=32):
        '''获取Cookie，默认使用H5的token名称，然后取32位'''
        return self.cookies.get(name,domain=domain)[start:end] if self.cookies.get(name,default='',domain=domain) else ''

    def cookstr2dict(self,CookieStr:str):
        '''将从浏览器获取到cookie字符串转成字典'''
        ls = CookieStr.replace(' ','').split(';')
        return OrderedDict(list(map(lambda x:re.split(r'=',x,1),ls)))
        # 这种方式也可以直接转换
        # cookie = SimpleCookie()
        # cookie.load(CookieStr)
        # return cookie
    
    def console(self,log_options:dict={}):
        '''日志输出设置
        日志的输出格式为：行号 时间 级别::路径->文件名->函数名=>消息
        日志添加两个：一个是文本日志记录，一个用于控制台输出
        '''
        log_config = OrderedDict({
            'level':logging.ERROR,
            'filename':'',
            'datefmt':'%Y-%m-%d %H:%M:%S',
            'filemode':'a',
            'format':'%(lineno)d %(asctime)s@%(levelname)s::%(pathname)s->%(filename)s->%(funcName)s=>%(message)s'
        })
        log_config.update(log_options) if log_options else None
        logging.basicConfig(**log_config)
        file_log = logging.FileHandler(Path.joinpath(Path.cwd(),f'{Path(__file__).name.split(".")[0]}-log.txt'))

        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)
        logger.addHandler(file_log)
        logger.addHandler(console_log)

    
    def h5_sign(self,token:str,t:str,appkey:str,data:str,Binary:bool=False):
        '''加密方式采用淘宝H5网页的加密流程
        data传递使用的是字符串，一是为了少加密一次，二是为了直接说明这个要转成json字符串，还需要去掉空格
        '''
        func = 'digest' if Binary else 'hexdigest'
        sign_str = f'{token}&{t}&{appkey}&{data}'
        return getattr(md5(sign_str.encode('utf-8')),func)()
    
    def open_Hmacsign(self,secret:'密钥信息',sign_data:dict,Binary:bool=False):
        '''淘宝开放平台的加密流程:hmac加密'''
        ls = sorted(sign_data.items(),key=lambda x:x)
        sign_str = ''.join(list(map(lambda x:''.join(x),ls)))
        func = 'digest' if Binary else 'hexdigest'
        return getattr(HMAC(secret.encode('utf-8'),sign_str.encode('utf-8')),func)().upper()
    
    def open_Md5sign(self,secret:str,sign_data:dict,Binary:bool=False):
        '''淘宝开放平台的加密流程:md5加密'''
        ls = sorted(sign_data.items(),key=lambda x:x)
        sign_str = ''.join(list(map(lambda x:''.join(x),ls)))
        func = 'digest' if Binary else 'hexdigest'
        return getattr(md5(f'{secret}{sign_str}{secret}'.encode('utf-8')),func)().upper()
        
    
    def app_sign(self,secret:'加密密钥'='',data:dict={},sign_func=sha1):
        '''猜想中的淘宝app加密方法，不过data应该也是要排序什么的吧，不过暂时是不清楚了，逆向不出来
        {v=1.0, deviceId=AiXb03Jh5K0C_vSLWC-u2MasOk_76QEfvIpiCMqJKlAl, appKey=21783927, sid=null, t=1545462522, data={"bizType":"taoPassword.judgePassword","bizParam":"{\"passwordContent\":\"comifengnewsclientgold:\\/\\/call?type=list\"}"}, api=mtop.taobao.aplatform.weakget, utdid=XBNj6B3lKccDAOjKwIsds5d9, x-features=27, uid=null, ttid=10035437@etao_android_8.8.8}
        现在已找到参数组合顺序
        '''

        def resovle(key_name):
            if data.get(key_name) == 'null':
                return ''
            elif not isinstance(data.get(key_name,''),str):
                dumpStr = json.dumps(data.get(key_name),separators=(',',':'))
                if key_name == 'data':
                    return md5(dumpStr.encode()).hexdigest()
                else:
                    return dumpStr
            else:
                return data.get(key_name,'')
        keyword_ls = ['utdid','uid','reqbiz-ext','appKey','data','t','api','v','sid','ttid','deviceId','lat','lng','x-features']
        if data.get('extdata'):
            keyword_ls.insert(-1,'extdata')
        dt = list(map(resovle,keyword_ls))
        sign_str = '&'.join(dt)

        return HMAC(f'{secret}'.encode('utf-8'),sign_str.encode('utf-8'))
    
    def map2str(self,paramData:dict):
        '''转换传递的字典为连接字符串'''
        def resovle(key_name):
            if paramData.get(key_name) == 'null':
                return ''
            elif not isinstance(paramData.get(key_name,''),str):
                dumpStr = json.dumps(paramData.get(key_name),separators=(',',':'))
                if key_name == 'data':
                    return md5(dumpStr.encode()).hexdigest()
                else:
                    return dumpStr
            else:
                return paramData.get(key_name,'')
        
        keyword_ls = ['utdid','uid','reqbiz-ext','appKey','data','t','api','v','sid','ttid','deviceId','lat','lng','x-features']
        if paramData.get('extdata'):
            keyword_ls.insert(-1,'extdata')
        data = list(map(resovle,keyword_ls))
        sign_str = '&'.join(data)
        
        return sign_str
    
    def addHeader(self,headers:dict={}):
        default_headers = {
            'x-mini-wua':'HHnB_3P3rpjjITYyMfTtldI+UFRpOScjy799La90R\/mybecdU56yAvaqEmEy46f5uQUCDcnIiqfJxLzP4vM0BxDClP8zD\/6RHI1z8StNM6Uqo73b2GC7KN7bQuM\/fXcQeS463',
            'x-ttid':'700169@travel_android_9.2.5',
            'x-features-':'27',
            'x-appkey':'12663307',
            'x-pv':''
        }
        self.headers.update(default_headers)
        self.headers.update(headers)
        return


    # 不能使用静态方法来作为装饰器
    # @staticmethod 
    def retry(function,token_name:str='taobaoToken'):
        '''token重新获取装饰器，且token名可能更换,function是被装饰的函数'''

        # print(token_name,function)
        @functools.wraps(function)
        def decorator(self,*args,**kw):
            '''self现在变成了显式的传递'''
            # print(args,kw)
            url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=100&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&dt=1&specialTxt=3&specialJson='
            if not hasattr(self,'_proxy'):
                self._proxy = {'time':datetime.datetime.now(),'proxy':self.__get_proxy(url)}
            try:
                res = function(self,*args,**kw)
            except ProxyError as e:
                print(e,'代理无效')
                self._proxy.update({'time':datetime.datetime.now(),'proxy':self.__get_proxy(url)})
                print('代理IP切换')
                res = function(self,*args,**kw)
            if 'FAIL_SYS_TOKEN_EMPTY' in res:
                self.app_config['taobaoToken'] = self.getToken()
                return function(self,*args,**kw)
            elif 'FAIL_SYS_USER_VALIDATE' in res or (datetime.datetime.now().minute - self._proxy['time'].minute):
                #代理IP检查，如果返回的数据不是正常的，或者是代理IP的使用时间到了1分钟，则切换代理IP
                self._proxy.update({'time':datetime.datetime.now(),'proxy':self.get_proxy(url)})
                print('代理IP切换')
                return function(self,*args,**kw)
            return res
        return decorator
    

    # def start_thread(self,func,**kw):
    #     '''启动一个暗中运行的线程
    #     接受一个函数，然后传递其他参数决定在什么时候运行，以及运行的次数
    #     但是现在是无法访问停止状态，线程里面的函数如果没有显示的监听那么将会访问不到停止状态，不能从外部停止
    #     感觉没个鸟用
    #     '''
    #     def run(func,**args){
    #         times = args.get('times',1)
    #         interval = args.get('seconds',1)
    #         while times and self.stop_event.isSet():
    #             times -= 1
    #             func(*args.get('args',()))
    #             self.stop_event.wait(interval)
    #     }
    #     thread = Thread(target=run,args=(func,),kwargs=kw)
    #     return thread   


    def addLogger(self,name:str,callback:'回调函数'=None):
        '''添加日志监听器
        name是属性名或者是函数名
        callback是匹配到名称之后如果有设置回调函数则返回回调函数
        '''
        pass   

    def hex2Base64(self,t):
        ''' 支付宝的js方法，改写'''
        o = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        e = 0
        n = ''
        r = ''
        for e in range(0,len(t),3):
            if e + 3 >= len(t):
                break
            n = int(t[e:e + 3],16)
            r += o[n >> 6] + o[63 & n]

        if e + 1 == len(t):
            n = int(t[e:e + 1],16)
            r += o[n << 2]
        elif e + 2 == len(t):
            n = int(t[e:e + 2],16)
            r += o[n >> 2] + o[(3 & n) << 4]
        while 3 & len(r) > 0:
            r += '='
        return r

    def encrypt(self,t:str):
        ''' 支付宝加密方法'''
        t = t[:245]
        counter = 0
        e = ''
        while len(e) != 344 and counter < 10:
            pass
    
    def RSAencrypt(self,public_key:'公钥',sign_str:str,salt:'盐'=''):
        '''通过字符串公钥提取模数和指数生成公钥去加密'''
        modulus_num , exponent_num = self.str2key(public_key)
        modulus = int(modulus_num,16)
        exponent = int(exponent_num,16)
        rsa_pubkey = rsa.PublicKey(modulus,exponent)
        crypto = rsa.encrypt(sign_str.encode(),rsa_pubkey)
        crypto = b64encode(crypto)
        return crypto.decode()
    
    def str2key(self,ts:str):
        '''字符串公钥提取模数和指数'''
        # 对字符串解码
        b_str = b64decode(ts)

        if len(b_str) < 162:
            return False

        hex_str = ''
        # 按位转换成16进制
        for x in b_str:
            # h = hex(ord(x))[2:]
            h = hex(x)[2:]
            h = h.rjust(2, '0')
            hex_str += h

        # 找到模数和指数的开头结束位置
        m_start = 29 * 2
        e_start = 159 * 2
        m_len = 128 * 2
        e_len = 3 * 2

        modulus = hex_str[m_start:m_start + m_len]
        exponent = hex_str[e_start:e_start + e_len]

        return modulus,exponent
    
    def alipay_umdata(self,login_url:str,appname:str,view_height:int=700,view_width:int=400,ips:str='192.168.10.10',headers:dict={}):
        '''获取支付宝的umdata参数'''

        url = 'https://ynuf.alipay.com/service/um.json'
        self.um_payload.update({
            'bsh':view_height,
            'bsw':view_width,
            'sah':view_height,
            'saw':view_width,
            'sh':view_height,
            'sw':view_width,
            'ett':int(round(time() * 1000))
        })

        self.um_payload.update({
            'eloc':quote(login_url),
            'xa':appname,
            'xt':self.cookies.get('umt')
        })
        encode_str = b64encode(json.dumps(self.um_payload,separators=(',',':')).encode()).decode()
        res = self.post(url,data={'data':'ENCODE~~V01~~' + encode_str},headers=headers)
        return res
        


if __name__ == '__main__':
    base = Base()
    res = base.app_sign('aa',data={'v': '1.0', 'deviceId': 'AiXb03Jh5K0C_vSLWC-u2MasOk_76QEfvIpiCMqJKlAl', 'appKey': '21783927', 'sid': 'null', 't': '1545462522', 'data': {}, 'api': 'mtop.taobao.aplatform.weakget', 'utdid': 'XBNj6B3lKccDAOjKwIsds5d9', 'uid': 'null', 'ttid': '10035437@etao_android_8.8.8', 'x-features': 27})
    print(res)


    

