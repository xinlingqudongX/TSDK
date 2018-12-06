# coding:utf-8

#   此文件的目的是能够让API配置直接加载到主类上面，产生函数

from 配置加载 import FileSystem
from hashlib import md5
from time import time
from urllib.parse import *
from requests import *
from random import choice
import hashlib
import hmac
from datetime import datetime
import logging

import apscheduler
import json
import fake_useragent
import collections




class Mtop(object):

    def __init__(self,updata:dict={},SDK:dict={},Error:dict={}):
        '''构建请求类，用于网络请求的构建'''
        self.request = Dt({
            'req':Session(),
            'head':{
                'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                'x-requested-with':'XMLHttpRequest',
                'origin':'https://h5.m.taobao.com',
                'referer':'https://h5.m.taobao.com'
            }})
        self.data = updata
        # for name in  config:
        #     setattr(self,name,config.get(name))
        
        self.__dt_name = {
            '淘宝H5':Func,
            '淘宝开放平台':TaobaoPlatform,
            '通常性API':Tfunc,
        }

        for sdk_typename in res.get('SDK'):
            config = res.get('SDK')[sdk_typename].pop('config',{})
            self[sdk_typename] = config
            for Func_name in res.get('SDK')[sdk_typename]:
                self.__dt_name[sdk_typename](Func_name,res.get('SDK')[sdk_typename][Func_name],register=self.regist)
            
        
        #请求的初始化，为了在最开始的时候获取到淘宝的cookie
        self.__login()
        
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    def _getconfig(self,obj):
        data = list(filter(lambda ls:ls[0] if isinstance(obj,ls[1]) else None,self.__dt_name.items()))
        if data:
            return self[data[0][0]]
        else:
            return {}
    
    def __login(self,start_url:str=''):
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/'
        self.request.req.get(url)
        self.rload()
        return
    
    def console(self,outpath,filename):
        pass
    
    def cookstr2dict(self,CookieStr:str):
        ls = CookieStr.replace(' ','').split(';');
        return collections.OrderedDict(list(map(lambda x:re.split(r'=',x,1),ls)))
    
    def MD5_sign(self,data,Binary:bool=False):
        md5 = hashlib.md5(data.encode())
        name = 'digest' if Binary else 'hexdigest'
        return getattr(md5,name)()
    
    def getUmidToken(self)->str:
        return 'C' + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(11)) + str(int(time() * 1000)) + ''.join(str(choice(range(10))) for _ in range(3))
    
    def params(self,**kw):
        '''生成请求的参数'''
        return urlencode(kw)
    
    def getpath(self,url:str='',**kw):
        '''生成请求的初始链接'''

        return f'{kw.get("domain")}/{kw.get("path")}/{url if url else ""}'
    
    def sign(self,token:str,t:str,appkey:str,data:str,Binary:bool=False):
        '''H5淘宝算法的加密'''
        # data = json.dumps(data,separators=(',',':'))
        return md5(f'{token}&{t}&{appkey}&{data}'.encode('utf-8')).hexdigest()
    
    def getCookie(self,name:str="_m_h5_tk",start:int=0,end:int=32):
        '''获取Cookie，默认使用H5的token名称，然后取32位'''
        return self.request.req.cookies.get(name,'')[start:end]
    
    def rload(self,url:str=''):
        url = url if url else 'https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478'
        res = self.request.req.get(url)

    # @classmethod
    def regist(self,name,func_object):
        '''注册函数对象到对象上，然后将对象赋值为函数的属性'''
        self[name] = func_object
        return self
    
    def res_check(self,res):
        dt = res.headers


    def err_resolve(self,res):
        '''检查返回数据的返回值，如果不是正常的那么就提示'''
        res = json.loads(res)
    
    def makeUrl(self,**options):
        '''接收参数然后生成API访问链接地址,'''
        
        method = options.pop('method','get')
        config = options.pop('config')
        # if method == 'post':
        #     data = options.pop('data',{})
        # else:
        #     data = options.get('data',{})
        data = options.pop('data',{})
        params = self.data.copy()
        params['data'] = json.dumps(data,separators=(',',':'))
        token = self.getCookie()
        if not token:
            self.rload()
            token = self.getCookie()
        t = int(time()*1000)
        sign = self.sign(**{'token':token,'t':t,'appkey':config.get('appkey','12574478'),'data':params['data']})
        
        url = self.getpath(options.pop('path',False),**config)

        params.update(options)
        params.update({
            't':t,
            'sign':sign
        })
        

        return {'url':url,'params':params,'data':json.dumps(data,separators=(',',':')),'method':method}
    
    def getres(self,options,head:dict={}):
        '''通过传递的数据进行判断需要使用什么请求'''
        method = options.pop('method','get')
        res = getattr(self.request.req,method.lower())(**options,headers= head if head else self.request.head)
        try:
            return json.loads(res.text)
        except Exception as e:
            return {'success':False,'data':res.text,'err':e}



class Func(object):

    def __init__(self,name,options,register=Mtop.regist):
        '''淘宝API'''
        self.name = name
        for item in options:
            value = options.get(item,'')
            if isinstance(value,dict):
                dt = collections.OrderedDict()
                dt.update(value)
                setattr(self,item,dt)
            else:
                setattr(self,item,value)
        self.path = f'{options.get("api","")}/{options.get("v","")}'
        self.method = self.method if hasattr(self,'method') else 'get'
        self.mtop = register(self.name,self)

    def params_check(self,options:dict=collections.OrderedDict()):
        options = collections.OrderedDict(options)
        if hasattr(self,'data'):
            for item_name in self.data:
                if not options.get(item_name,None):
                    if isinstance(self.data[item_name],bool):
                        if self.data[item_name]:
                            raise Exception(f'缺少要的参数：{item_name}')
                        else:
                            options.pop(item_name,'')
                    else:
                        options.update({item_name:self.data[item_name]})

        return options

    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    
    def __call__(self,head:dict={},**data):
        '''接收参数并参与加密'''
        if not hasattr(self,'mtop'):
            return 
        data = self.params_check(data)
        options = {'method':self.method,'api':self.api,'data':data,'v':self.v,'path':self.path,'config':self.mtop._getconfig(self)}
        payload = self.mtop.makeUrl(**options)
        print(payload)
        return self.mtop.getres(payload)
    
    def call(self,**kw):
        '''接收参数并修改原本的参数进行替换'''
        for attr_name in kw:
            setattr(self,attr_name)


class Tfunc(object):

    def __init__(self,name,options,register=Mtop.regist):
        '''通常的API'''
        self.name = name
        self.params = {
                "adUrl":{"default":""},
                "adImage":{"default":""},
                "adText":{"default":""},
                "viewFd4PC":{"default":""},
                "viewFd4Mobile":{"default":""},
                "form":{"default":"tb"},
                "appkey":{"default":"00000000"},
                "umid_token":{"must":True}
            }
        self.mtop = register(self.name,self)
    
    def getParams(self,options:dict={})->dict:
        '''对参数进行检查，然后对默认参数赋值，必要参数缺少报错，特殊参数去除'''
        if hasattr(self,'params'):
            for key in self.params:
                if not options.get(key,None):
                    if isinstance(self.params[key],bool):
                        if self.params[key]:
                            raise Exception(f'缺少参数:{key}') if not options.get(key,None) else print('check done')
                        else:
                            options.pop(key,None)
                    else:
                        options.update({key:self.params[key]})
        
        return options
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
        
    
    def __call__(self,**options):
        params = self.getParams(options)
        res = self.mtop.getres({'params':params,'method':self.method,'url':self.url})
        return res



class TaobaoPlatform(object):
    
    def __init__(self,name:str="",app_key:str="",secret:str="",protocol:str='https',sandbox:bool=False,sign_method:str="md5",register=Mtop.regist):
        '''淘宝开放平台，主体配置设置'''
        self.name = name
        self.SandboxURL = 'http://gw.api.tbsandbox.com/router/rest'
        self.formalURL = 'https://eco.taobao.com/router/rest'
        # self.OverseasURL = 'http://api.taobao.com/router/rest'
        self.req_url = self.SandboxURL if sandbox else self.formalURL
        # self.app_key = app_key
        # self.secret = secret
        # self.sign_method = sign_method
        # self.protocol = protocol

        self.config = collections.OrderedDict({
            'sandbox':sandbox,
            'protocol':protocol,
            'sign_method':sign_method,
            'app_key':app_key,
            'secret':secret
        })
        # self.mtop = register(self.name,self)
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    def getPayload(self,time_format:str="%Y-%m-%d %H:%M:%S"):
        return collections.OrderedDict({
            'app_key':self.config.app_key,
            'sign_method':self.config.sign_method,
            'timestamp':datetime.now().strftime(time_format),
            'v':'2.0',
            'format':'json'
        })
    
    def md5(self,sign_str:str):
        return hashlib.md5(f'{self.secret}{sign_str}{self.secret}'.encode('utf-8')).hexdigest()
    
    def hmac(self,sign_str:str,sign_func=hashlib.md5):
        return hmac.HMAC(f'{self.secret}'.encode(),sign_str.encode('utf-8'),sign_func).hexdigest()
    
    def sign(self,data):
        ls = sorted(data.items(),key=lambda x:x)
        value = ''.join(list(map(lambda x:''.join(x),ls)))
        return self[self.sign_method](value)

    def params_check(self,data:dict):
        if hasattr(self,'params'):
            for item_name in self.params:
                if not self.params.get(item_name,None):
                    if isinstance(self.params[item_name],bool):
                            if self.params[item_name]:
                                raise Exception(f'缺少参数:{item_name}')
                            else:
                                data.pop(item_name,None)
                    else:
                        data.update({item_name:self.params[item_name]})
        return collections.OrderedDict(data)
    
    def getitem(self,itemid):
        payload = collections.OrderedDict({
            "fields":"num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick",
            "q":'雨伞',
            "cat":"16,18"
        })
        dt = self.getPayload()
        payload.update(dt)
        payload.update({'method':'taobao.tbk.item.get'})

        res = self.sign(payload)    
        payload.update({'sign':res})
        req = post(self.formalURL,data=payload)
        return req.text

    def __call__(self,**data):

        pass


class Dt(object):

    def __init__(self,options):
        for item in options:
            setattr(self,item,options.get(item))
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)


if __name__ == '__main__':

    
    fs = FileSystem()
    res = fs.getjson()

    mtop = Mtop(**res)
    mtop._getconfig(mtop.淘抢购)
    # print(res)
    mtop = Mtop(res['domain']['H5'],res['setting'])
    for api_name in res['taobao']:
        mtop.regist(api_name,Func(api_name,res['taobao'].get(api_name)))
    for api_name in res['通常']:
        mtop.regist(api_name,Tfunc(api_name,res['通常'][api_name]))
    for api_name in res['淘宝开放平台']:
        mtop.regist(api_name,)
    # res = mtop.宝贝详情(itemNumId='555737987405')
    # res = mtop.淘抢购()
    # res = mtop.喵口令(**{'tmallShare': '{"content":"fiona+chen\\/斐娜晨秋季新款时尚撞色印花抽绳连帽长袖外套女","title":"fionachen斐娜晨旗舰店","requireTmall":false,"utSk":"1.W4d7R8qEOy0DAFAPLFNrh2h1_23181017_1542348172.18.detail","actionRule":[{"platform":"tmall","url":"\\/\\/a.m.tmall.com\\/i577362725601.htm","version":"*"},{"platform":"*","url":"\\/\\/a.m.tmall.com\\/i577362725601.htm","version":"*"}],"bizLogo":"¥1999","backgroundImg":"http:\\/\\/img.alicdn.com\\/imgextra\\/i2\\/2906465954\\/O1CN01ulHxba1tqyeEYmpsf_!!0-item_pic.jpg","bizName":"detail","type":18,"channel":"MIAO_KOULING","bizId":"577362725601","ext":{"hasLottery":false,"itemIds":[],"isWebview":false,"batchShareType":"","itemId":577362725601,"sellerId":2906465954}}'})
    # res = mtop.淘口令()
    # res = mtop.测试2(**{'msCodes':'2018061501','params':'{"catId":"1495"}'})
    # print(res)

    pc = TaobaoPlatform('25263570','36b3bddb45f177575f63511b54c9e655')
    res = pc.getitem('1234565')
    # print(res)