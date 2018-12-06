# coding:utf-8

import 函数对象包
from 函数对象包.SDK基类 import Base
from requests import Session
from collections import OrderedDict



class Taobao(Base,Session):
    '''
    作用：从函数对象包中导出所有的函数对象，然后挂载到当前对象上面，
    再添加一个共同对象的路由
    '''

    def __init__(self):
        super(Taobao,self).__init__()
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    def __getattr__(self,name):
        if hasattr(self,name):
            return self[name]
        elif hasattr(self.mtop,name):
            return self.mtop[name]
    
    @property
    def url(self):
        # self.req_config = OrderedDict({
        #     'method':'',
        #     'domain':'',
        #     'path'
        # })
        return 
