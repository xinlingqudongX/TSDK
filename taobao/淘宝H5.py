# coding:utf-8

from __future__ import absolute_import


try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base

from time import time
import json
from collections import OrderedDict



class TB_H5(Base):
   
    def __init__(self,config={
        "domain":"https://h5api.m.taobao.com",
        "path":"h5",
        "appkey":"12574478",
        "loginURL":"https://login.taobao.com/member/login.jhtml",
        "redirectURL":"https://www.taobao.com/",
        "method":"get"
    }):
        super(TB_H5,self).__init__()
        self.config = config
        self.__first()
    
    def execute(self,datas:dict):

        data = datas.pop('data',{})
        data_str = json.dumps(data,separators=(',',':'))
        t = str(int(time() * 1000))
        appkey = self.config.get('appkey')
        sign = self.h5_sign(self.getCookie(),t,appkey,data_str)
        datas.update({'sign':sign,'data':data_str,'t':t,'appkey':appkey})

        options = OrderedDict()
        options['method'] = datas.get('method','get')
        if self.config.get('path').find('/rest/') > -1:
            url = '/'.join([self.config.get('domain'),self.config.get('path')])
        else:
            url = '/'.join([self.config.get('domain'),self.config.get('path'),datas.get('api').lower(),datas.get('v')])
        options['url'] = url
        if options['method'] == 'get':
            options['params'] = datas
        else:
            options['data'] = datas
        res = self.request(**options)
        return res
    
    
    def __first(self,url:str="https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
        '''必须首先请求一个api来获取到h5token'''
        res = self.get(url)
        return res


if __name__ == '__main__':

    tb = TB_H5({
        "domain":"https://h5api.m.taobao.com",
        "path":"h5",
        "appkey":"12574478",
        "loginURL":"https://login.taobao.com/member/login.jhtml",
        "redirectURL":"https://www.taobao.com/",
        "method":"get"
    })
    res = tb.execute({
        'api':'mtop.taobao.detail.getdetail',
        'v':'6.0',
        'jsv':'2.4.8',
        'dataType':'json',
        'type':'json',
        'ttid':'2017%40taobao_h5_6.6.0',
        'AntiCreep':'true',
        'data':{
            'itemNumId':'585559878166'
        }
    });
    print(res.text)