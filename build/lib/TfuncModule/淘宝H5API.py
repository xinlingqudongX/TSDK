# coding:utf-8

try:
    from . SDK基类 import Base
except ModuleNotFoundError:
    from SDK基类 import Base
from requests import Session
from time import time
import json
from urllib.parse import quote



class 淘宝H5(Base):

    def __init__(self,name:str,config:dict={},req_config:dict={}):
        '''
        config是对象的参数公共配置
        req_config是参数请求公共配置
        '''
        super(淘宝H5,self).__init__()
        self.config = config
        self.req_config = req_config
        self.mtop = Session()
        self.__first()
    
    
    @property
    def url(self):
        domain = self.config.get('domain','https://h5api.m.taobao.com')
        path = self.config.get('path','h5')
        api = self.req_config.get('api')
        v = self.req_config.get('v')
        return '/'.join([domain,path,api,v])
    
    def __first(self,url:str="https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
        '''必须首先请求一个api来获取到h5token'''
        self.request('get',url) if hasattr(self,'request') else self.mtop.get(url)

    
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
        token = self.getCookie() or (self.cookies.get('_m_h5_tk')[:32] if hasattr(self,'request') else self.mtop.cookies.get('_m_h5_tk')[:32]) 
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

        res = self.request(**dt) if hasattr(self,'request') else self.mtop.request(**dt)
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