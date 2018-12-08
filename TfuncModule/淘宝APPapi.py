try:
    from . SDK基类 import Base
except ModuleNotFoundError:
    from SDK基类 import Base
from requests import Session

class 淘宝APP(object):

    def __init__(self,name:str,config:dict,req_config:dict):
        self.config = config
        self.req_config = req_config
        self.mtop = Session()
    
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
    
    def getres(self,params:dict):
        pass
        res = self.request(**options) if hasattr(self,'request') else self.mtop.request(**options)
    
    def __call__(self,**kw):
        pass


if __name__ == "__main__":
    ts = 淘宝APP()