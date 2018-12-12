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


class Base(object):
    '''工具类的基类：
        功能：淘宝h5md5加密
            淘宝hmac加密，暂时未知真实加密步骤
            生成URL对象
            生成requests参数对象
    '''
    __public__ = []

    def __init__(self):
        # self.req_config = OrderedDict({
        #     'method':'',
        #     'domain':'',
        #     'path'
        # })
        self.console()
    

    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    def __getattr__(self,name):
        '''属性访问器，当通过这个来访问的时候，判断
        有没有mtop属性，有的时候返回taobao对象的方法
        改用公共对象的方法访问，用于以后扩展需要
        '''
        #判断公共对象是否有这个属性，没有则报错
        if self.__public__:
            obj = list(filter(lambda obj:hasattr(obj,name),self.__public__))
            if obj:
                return obj[0][name]
            else:
                raise AttributeError
        else:
            raise AttributeError
    
    def __get_proxy(self,url):
        res = self.mtop.get(url,timeout=10)
        ip_json = json.loads(res.text)
        if ip_json['success'] == 'true' or ip_json['success']:
            print(ip_json)
            data = list(map(lambda item:f'http://{item["IP"]}',ip_json['data'])).pop()
            return {'http':data,'https':data}
        else:
            print(res.text)
            print('获取代理ip出错')
            return 
    
    @classmethod
    def regist(cls,mtop:'主要调用对象的实例'=object,*args,**kw):
        '''返回当前类的实例，然后把传递进来的参数存放在公共存储位置，用于请求的访问'''
        cls.mtop = mtop
        cls.__public__.append(mtop)
        return cls(*args,**kw)
    


    @property
    def url(self):
        return urljoin(self.req_config['domain'],self.req_config['path'])

    
    def getUmidToken(self)->str:
        return 'C' + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(11)) + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(3))
    
    def getCookie(self,name:str="_m_h5_tk",start:int=0,end:int=32):
        '''获取Cookie，默认使用H5的token名称，然后取32位'''
        if hasattr(self,'cookies'):
            return self.cookies.get(name,'')[start:end]
        else:
            return ''

    def cookstr2dict(self,CookieStr:str):
        '''将从浏览器获取到cookie字符串转成字典'''
        ls = CookieStr.replace(' ','').split(';')
        return OrderedDict(list(map(lambda x:re.split(r'=',x,1),ls)))
    
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
        '''猜想中的淘宝app加密方法，不过data应该也是要排序什么的吧，不过暂时是不清楚了，逆向不出来'''
        return HMAC(f'{secret}'.encode('utf-8'),json.dumps(data,separators=(',',':')).encode('utf-8'))

    @staticmethod
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



if __name__ == '__main__':
    base = Base()


    

