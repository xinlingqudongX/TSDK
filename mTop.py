# coding:utf-8


from TfuncModule.淘宝APPapi import 淘宝APP
from TfuncModule.淘宝H5API import 淘宝H5
from TfuncModule.淘宝开放平台API import 淘宝开放平台
from TfuncModule.淘宝通用API import 淘宝通用
from TfuncModule.SDK基类 import Base
from requests import Session
from collections import OrderedDict
from pathlib import Path
import json



class Taobao(Session,Base):
    '''
    作用：从函数对象包中导出所有的函数对象，然后挂载到当前对象上面，
    再添加一个共同对象的路由
    '''

    def __init__(self):
        super(Taobao,self).__init__()
        Base.__init__(self)
        self.api_config = self.__getConfig()
        self.__LoadObj(self.api_config.get('SDK',{}))
    
    def __getitem__(self,name):
        return getattr(self,name)
    
    def __setitem__(self,name,val):
        setattr(self,name,val)
    
    def __getConfig(self,path:str='./Api.json'):
        if Path(path).exists():
            with open(path,encoding='utf-8') as f:
                dt = json.load(f)
            return dt
        else:
            return {}
    
    def __LoadObj(self,configObj,base:object=Base):
        base.__public__.append(self)
        for item_name in configObj:
            if globals().get(item_name,None):
                if item_name == '淘宝开放平台':
                    
                    user_config = configObj[item_name].pop('user_config',{})
                    env = configObj[item_name].pop('env',{})
                    for func_name in configObj[item_name]:
                        #淘宝开放平台API注册
                        self[func_name] = globals()[item_name](name=func_name,user_config=user_config,env=env,req_config=configObj[item_name][func_name])
                elif item_name == '淘宝通用':
                    for func_name in configObj[item_name]:
                        #淘宝通用API注册
                        self[func_name] = globals()[item_name](name=func_name,options=configObj[item_name][func_name])
                elif item_name == '淘宝H5':
                    config = configObj[item_name].pop('config',{})
                    for func_name in configObj[item_name]:
                        #淘宝H5API注册
                        self[func_name] = globals()[item_name](name=func_name,config=config,req_config=configObj[item_name][func_name])
                elif item_name == '淘宝APP':
                    config = configObj[item_name].pop('config',{})
                    for func_name in configObj[item_name]:
                        #淘宝APPAPI注册
                        self[func_name] = globals()[item_name](name=func_name,config=config,req_config=configObj[item_name][func_name])
                else:
                    pass
    



if __name__ == '__main__':
    
    mtop = Taobao()
    mtop.我的足迹()