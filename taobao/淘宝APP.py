# coding:utf-8

from __future__ import absolute_import


try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base
from collections import OrderedDict

class TB_APP(Base):

    def __init__(self,name:str,config:dict,req_config:dict):
        '''淘宝app类暂时不做更改，因为暂时也是无用'''
        self.config = config
        self.req_config = req_config
        self.mtop = Session()
        super(TB_APP,self).__init__()
    
    def __tb_appInfo(self):
        state_info = {
            'KEY_ACCESS_TOKEN':'accessToken',
            'KEY_API':'api',
            'KEY_APPKEY':'appKey',
            'KEY_APP_BACKGROUND':'AppBackground',
            'KEY_CURRENT_PAGE_NAME':'PageUrl',
            'KEY_CURRENT_PAGE_NAME':'PageName',
            'KEY_DATA':'data',
            'KEY_DEVICEID':'deviceId',
            'KEY_EXTDATA':'extdata',
            'KEY_LAT':'lat',
            'KEY_LNG':'lng',
            'KEY_MTEE_UA':'ua',
            'KEY_NETTYPE':'netType',
            'KEY_NQ':'nq',
            'KEY_PV':'pv',
            'KEY_REQBIZ_EXT':'reqbiz-ext',
            'KEY_SG_ERROR_CODE':'SG_ERROR_CODE',
            'KEY_SID':'sid',
            'KEY_SIGN':'sign',
            'KEY_TIME':'t',
            'KEY_TIME_OFFSET':'t_offset',
            'KEY_TTID':'ttid',
            'KEY_TYPE':'type',
            'KEY_UA':'ua',
            'KEY_UID':'uid',
            'KEY_UMID_TOKEN':'umt',
            'KEY_UTDID':'utdid',
            'KEY_VERSION':'v',
            'KEY_WUA':'wua',
            'VALUE_TIME_OFFSET':'0',
            'VALUE_PRODUCT_PV':'1.0',
            'VALUE_OPEN_PV':'1.0',
            'VALUE_INNER_PV':'5.1',
            'KEY_X_FEATURES':'x-features',

        }
    
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
    
    def appsign(self):
        dt = OrderedDict()
        dt.update({
            'utdid':'W4d7R8qEOy0DAFAPLFNrh2h1',
            'uid':'',
            'reqbiz-ext':'',
            'data':'',
            't':'',
            'api':'',
            'v':'',
            'sid':'',
            'ttid':'10035437%40etao_android_8.8.6',
            'deviceld':'AnQezS1fsBjqX0zUCeXSMm5HlPCH5TJRP7Xl6-fG1p5K',
            'lat':'',
            'lng':'',
            'x-features':''
        })
    
    def __call__(self,**kw):
        pass


if __name__ == "__main__":
    ts = 淘宝APP()