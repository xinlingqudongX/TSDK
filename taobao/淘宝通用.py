# coding:utf-8

from __future__ import absolute_import


from .SDK基类 import Base
from collections import OrderedDict
from requests import Session


class 淘宝通用(Base):
    '''淘宝通用性API，是可以直接访问并返回需要的数据的API
    创建一个解析器，解析通用配置文件的数据转化成参数数据
    '''
    def __init__(self,name:str,options:dict):
        '''接受配置参数作为内置参数'''
        super(淘宝通用,self).__init__()
        self.name = name
        self.mtop = Session()
        self.options = options
    
    def params_check(self,params:dict={}):
        '''参数检查
        如果检查参数缺少但是配置参数是真的话，报错提示缺少必要的参数
        如果检查参数缺少但是配置参数假的话，暂时未定义
        如果检查参数缺少但是配置参数有默认的话，添加到参数上
        '''
        options = self.options.get('params',[])

        for item in options:
            if item.get('required',False) and not params.get(item.get('name'),False):
                raise Exception(f'缺少必要的参数：{item.get("name")}')
            elif not item.get('required',False) and params.get(item.get('name'),False):
                pass
            elif not item.get('required',False) and not params.get(item.get('name'),False):
                params[item.get('name')] = item.get('value','')
            else:
                pass
        return params
    
    def getres(self,params:dict):
        options = {
            'url':self.options.get('url'),
            'method':self.options.get('method','get')
        }
        if options.get('method') == 'get':
            options['params'] = params
        else:
            options['data'] = params

        res = self.request(**options) if hasattr(self,'request') else self.mtop.request(**options)
        return res
    
    def __call__(self,options:'新的配置信息'={},**kw):
        '''接受配置参数作为新的内置参数，用一个关键字参数作为更新参数'''
        if options:
            self.options.update(options)
        kw = self.params_check(kw)
        res = self.getres(kw)
        return res




if __name__ == '__main__':
    tb = 淘宝通用('获取登录二维码',options={
                "url":"https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do",
                "method":"get",
                "params":[
                    {
                        "name":"adUrl",
                        "value":""
                    },
                    {
                        "name":"adImage",
                        "value":""
                    },
                    {
                        "name":"adText",
                        "value":""
                    },
                    {
                        "name":"viewFd4PC",
                        "value":""
                    },
                    {
                       "name":"viewFd4Mobile",
                       "value":"" 
                    },
                    {
                        "name":"form",
                        "value":"tb"
                    },
                    {
                        "name":"appkey",
                        "value":"00000000"
                    },
                    {
                        "name":"umid_token",
                        "value":"",
                        "required":True
                    }
                ]
            })
    res = tb(umid_token='HV02PAAZ0b080a8b3a13174c5c08d77800e5dec1000999')    
    print(res)
        
