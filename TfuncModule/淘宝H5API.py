# coding:utf-8

try:
    from . SDK基类 import Base
except ModuleNotFoundError:
    from SDK基类 import Base
from requests import Session
from time import time
import json
from urllib.parse import quote
from collections import OrderedDict
from http.cookiejar import CookieJar



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
    
    @url.setter
    def url(self,url_value:'重新赋值的链接地址'):
        '''不过不能允许重新设置链接地址，因为这个地址是计算来的，重新赋值的话需要更改大量的配置'''
        pass

    
    def __first(self,url:str="https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
        '''必须首先请求一个api来获取到h5token'''
        self.request('get',url) if hasattr(self,'request') else self.mtop.get(url)

    
    def params_check(self,params:dict):
        '''参数检查
        参数的顺序和配置文件的顺序保持一致
        如果检查参数缺少但是配置参数是真的话，报错提示缺少必要的参数
        如果检查参数缺少但是配置参数假的话，暂时未定义
        如果检查参数缺少但是配置参数有默认的话，添加到参数上
        '''
        dt_params = OrderedDict()
        options = self.req_config.get('data',[])
        for item in options:
            if item.get('required',False) and not params.get(item.get('name'),False):
                raise Exception(f'缺少必要的参数：{item.get("name")}')
            elif not item.get('required',False) and params.get(item.get('name'),False):
                pass
            elif not item.get('required',False) and not params.get(item.get('name'),False):
                # params[item.get("name")] = item.get("value")
                dt_params.update({item.get("name"):item.get("value")})
            elif item.get('required',False) and params.get(item.get('name'),False):
                dt_params.update({item.get("name"):params.get(item.get("name"))})
            else:
                pass
        # return params
        return dt_params
    
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
        # token = self.getCookie() or (self.cookies.get('_m_h5_tk')[:32] if hasattr(self,'request') else self.mtop.cookies.get('_m_h5_tk',domain="")[:32]) 
        token = self.getCookie() or (self.cookies.get('_m_h5_tk')[:32] if hasattr(self,'request') else self.mtop.cookies.get('_m_h5_tk')[:32]) 
        appkey = self.req_config.get('appkey','12574478')
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
    # tb = 淘宝H5(name="获取订单详情1",config={
    #             "domain":"https://h5api.m.taobao.com",
    #             "path":"h5",
    #             "appkey":"12574478",
    #             "loginURL":"https://login.taobao.com/member/login.jhtml",
    #             "redirectURL":"https://www.taobao.com/"
    #         },req_config={
    #             "api":"mtop.order.querydetail",
    #             "v":"4.0",
    #             "jsv":"2.4.16",
    #             "appkey":"12574478",
    #             "ttid":"2018@taobao_h5_7.9.1",
    #             "isSec":0,
    #             "encode":0,
    #             "AntiFlood":"true",
    #             "AntiCreep":"true",
    #             "H5Request":"true",
    #             "type":"json",
    #             "dataType":"json",
    #             "data":[
    #                 {
    #                     "name":"appVersion",
    #                     "value":"1.0"
    #                 },
    #                 {
    #                     "name":"appName",
    #                     "value":"tborder"
    #                 },
    #                 {
    #                     "name":"bizOrderId",
    #                     "required":True
    #                 }    
    #             ]
    #         })
    tb = 淘宝H5(name="创建天猫订单",config={
                "domain":"https://h5api.m.taobao.com",
                "path":"h5",
                "appkey":"12574478",
                "loginURL":"https://login.taobao.com/member/login.jhtml",
                "redirectURL":"https://www.taobao.com/"
            },req_config={
                "method":"post",
                "api":"mtop.trade.buildorder.h5",
                "v":"3.0",
                "jsv":"2.4.7",
                "appkey":"12574478",
                "type":"originaljson",
                "AntiFlood":"true",
                "LoginRequest":"true",
                "H5Request":"true",
                "ttid":"#b#ad##_h5",
                "x-itemid":"576140975254",
                "x-uid":"1090955643",
                "data":[
                    {
                        "name":"itemId",
                        "required":True
                    },
                    {
                        "name":"quantity",
                        "value":1
                    },
                    {
                        "name":"buyNow",
                        "value":"true"
                    },
                    {
                        "name":"buyFrom",
                        "value":"tmall_h5_detail"
                    }
                ]
            })
    ck = tb.cookstr2dict("cna=j42mEyDenCcCAXE5RTDw/BLe; miid=8669944032109017482; thw=cn; tg=0; l=Avv7jGPLN1wJlaIVI/ccLE9WC9RlWQ9S; t=2c5512cb484aec662600a8e183d34e3b; cookie2=10395d19b3a00b80e0da1c57bc0c08aa; v=0; _tb_token_=f383b833b013e; ockeqeudmj=g6zqhKc%3D; munb=1090955643; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BtOk8uPHzsIAts45wZZtR1uc%3D; _w_app_lg=19; unb=1090955643; sg=%E7%84%B630; _l_g_=Ug%3D%3D; skt=9e23926ca2d5b5ea; uc1=cookie21=Vq8l%2BKCLiv0Mzbofagu7Fg%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie14=UoTYMhjc8f24HA%3D%3D; cookie1=Vv6fxNwYboXOnA3gl0xkAY1IBt4Q2MMC3HqyTw83URo%3D; csg=c313c02f; uc3=vt3=F8dByRzImMdnaNzUfBM%3D&id2=UoH2iZs9kSfwKw%3D%3D&nk2=sCJAj0Qx6%2FoezQ%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; tracknick=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136; lgc=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136; _cc_=U%2BGCWk%2F7og%3D%3D; dnk=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136; _nk_=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136; cookie17=UoH2iZs9kSfwKw%3D%3D; ntm=0; enc=4pLqhwGCBhn2rWk10fBZny%2B2RRxIs%2FXuG0dqxZLxM3KVENCoZgPsLh7EmMg%2Bb2Z4hk0asVfegfZWFwFIlTc1Ew%3D%3D; _m_h5_tk=112d7721247f51494f046308ac174777_1544700782531; _m_h5_tk_enc=f1fde7112af4a8ab6ef959a1b16480ef; isg=BEZGLpCQZkOptzWq_1BRts7BlzwID4sT0nVIezBvMmlEM-ZNmDfacSzFD2n_m4J5")
    tb.mtop.cookies.update(ck)
    # res = tb(bizOrderId='295914147223954356')
    # tb.mtop.proxies = {'http':'http://106.56.244.126:23300','https':'https://106.56.244.126:23300'}
    res = tb(itemId="576140975254")
    print(res)