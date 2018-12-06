# coding:utf-8

from SDK基类 import Base
from requests import Session
from time import time
import json
from urllib.parse import quote
import functools
import datetime

class 淘宝H5(Base):

    def __init__(self,name:str,config:dict={},req_config:dict={}):
        '''
        config是对象的参数公共配置
        req_config是参数请求公共配置
        '''
        self.config = config
        self.req_config = req_config
        self.mtop = self.mtop if hasattr(self,'mtop') else Session()
        self.__first()
    
    def __get_proxy(self,url):
        res = requests.get(url,timeout=10)
        ip_json = json.loads(res.text)
        if ip_json['success'] == 'true' or ip_json['success']:
            print(ip_json)
            data = list(map(lambda item:f'http://{item["IP"]}',ip_json['data'])).pop()
            return {'http':data,'https':data}
        else:
            print(res.text)
            print('获取代理ip出错')
            return 
    
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
            except requests.exceptions.ProxyError as e:
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
    
    @property
    def url(self):
        domain = self.config.get('domain','https://h5api.m.taobao.com')
        path = self.config.get('path','h5')
        api = self.req_config.get('api')
        v = self.req_config.get('v')
        return '/'.join([domain,path,api,v])
    
    def __first(self,url:str="https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
        '''必须首先请求一个api来获取到h5token'''
        self.mtop.get(url)

    
    def params_check(self,params:dict):
        '''参数检查
        如果检查参数缺少但是配置参数是真的话，报错提示缺少必要的参数
        如果检查参数缺少但是配置参数假的话，暂时未定义
        如果检查参数缺少但是配置参数有默认的话，添加到参数上
        '''
        options = self.req_config.get('data',[])
        for item in options:
            if item.get('required',False) and not params.get(item.get('name'),False):
                raise Exception(f'缺少必要的参数：{item.get("name")}')
            elif not item.get('required',False) and params.get(item.get('name'),False):
                pass
            elif not item.get('required',False) and not params.get(item.get('name'),False):
                params[item.get("name")] = item.get("value")
            else:
                pass
        return params
    
    def getres(self,options):
        '''获取返回的数据，如果有挂载对象就使用挂载对象，否则使用自己的请求
        之后的返回数据解析也会放在这个函数里面
        '''
        dt = {
            'method':self.req_config.get('method','get'),
            'url':self.url,
        }
        req_options = self.req_config.copy()
        req_options.update({'data':options})

        t = int(time() * 1000)
        token = self.getCookie() or self.mtop.cookies.get('_m_h5_tk')[:32]
        appkey = self.req_config.get('appkey','12547748')
        data = json.dumps(req_options.get('data',{}),separators=(",",":"))

        sign = self.h5_sign(token,t,appkey,data)
        req_options.update({
            'sign':sign,
            't':t,
            'data':data
        })

        if dt.get('method') is 'get':
            dt['params'] = req_options
        else:
            dt['data'] = req_options

        res = self.mtop.request(**dt)
        return res.text
    
    def __call__(self,options:dict={},**kw):
        if options:
            self.req_config.update(options)
        kw = self.params_check(kw)
        res = self.getres(kw)
        return res



if __name__ == '__main__':
    tb = 淘宝H5(name="宝贝规格信息",config={
                "domain":"https://h5api.m.taobao.com",
                "path":"h5",
                "appkey":"12547748",
                "loginURL":"https://login.taobao.com/member/login.jhtml",
                "redirectURL":"https://www.taobao.com/"
            },req_config={
                "api":"mtop.taobao.detail.getdesc",
                "dataType":"jsonp",
                "type":"json",
                "v":"6.0",
                "appKey":"12574478",
                "jsv":"2.5.0",
                "data":[
                    {
                        "name":"id",
                        "value":"14653261854",
                        "required":True
                    },
                    {
                        "name":"type",
                        "value":"0"
                    }
                ]
            })
    res = tb(id='558429704643')
    print(res)