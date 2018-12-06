# coding:utf-8

from SDK基类 import Base
import requests
from collections import OrderedDict
import time
import json

class 淘宝开放平台(Base):
    '''淘宝开放平台的API，用来解析开放平台的配置'''
    
    def __init__(self,name:'该函数的名称',user_config:'用户配置信息'={},env:"开放平台环境配置"={},req_config:'函数配置信息'={},**kw):
        '''接受两个配置，一个是用户配置信息，另一个是函数的参数配置信息'''
        #用户参数配置
        self.user_config = user_config
        #环境参数配置
        self.env = env
        #请求参数存放，然后需要对参数进行转换
        self.req_config = req_config
        #请求方式
        self.method = 'get' or 'post'
        self.publicParams();
    
    def publicParams(self,publicParams:dict=OrderedDict()):
        '''存放淘宝开放平台的公共参数，公共参数配置信息'''
        if publicParams:
            self._publicParams = publicParams
        else:
            _publicParams = OrderedDict()
            _publicParams['method'] = self.req_config.get('name','')
            _publicParams['app_key'] = self.user_config.get('appkey')
            _publicParams['sign_method'] = 'md5' or 'hmac'
            _publicParams['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            _publicParams['v'] = '2.0'
            _publicParams['format'] = 'json'
            self._publicParams = _publicParams

        return self._publicParams
    
    @property
    def url(self):
        '''通过配置信息获取到url'''
        protocol = self.env.get('protocol')
        sandbox = self.env.get('sandbox')
        url = self.env.get(sandbox).get(protocol)
        return url
    
    #不需要转换
    def conversion(self,requestPamams:list=[]):
        '''参数集转换成参数对象'''
        # self.req_config = OrderedDict()
        # for item in requestPamams:
        #     self.req_config.update({
        #         'fields':''
        #     })
        pass
    
    def params_check(self,params_obj:dict={}):
        '''参数对象检查
        如果参数配置里面有这个配置，且这个是必要的，但实际参数缺少，报错，提示缺少
        如果参数配置里面有这个配置，且这个是不必要的，但实际参数缺少，默认添加上
        是否添加上默认值这个暂时未确定
        '''
        for item in self.req_config.get('requestParams',[]):
            if item.get('required',False) and not params_obj.get(item.get('name')):
                raise Exception(f'缺少必要的参数：{item.get("name")},释义：{item.get("description")}')
            elif item.get('required',True) and params_obj.get(item.get('name'),True):
                # params_obj[item.get('name')] = item.get('value','')
                pass
            else:
                pass
        return params_obj

    
    def getres(self,params:dict):
        '''淘宝开放平台ok'''
        options = {
            'url':self.url,
            'method':self.method
        }
        public = self.publicParams()
        dt = {}
        dt.update(params)
        dt.update(public)
        
        if public.get('sign_method','md5') is 'md5':
            sign = self.open_Md5sign(self.user_config.get('appsecret'),dt)
        else:
            sign = self.open_Hmacsign(self.user_config.get('appsecret'),dt)
        dt['sign'] = sign
        options['params'] = dt
        if hasattr(self,'mtop'):
            req = self.mtop.request(**options)
        else:
            req = requests.request(**options)
        return req.text

    
    def __call__(self,options={},**kw):
        if options:
            self.req_config.update(options)

        kw = self.params_check(kw)
        #调用getres获取数据

        res = self.getres(kw)
        return res

        



if __name__ == '__main__':

    tb = 淘宝开放平台(**{
            "user_config":{
                "appkey":"25263570",
                "appsecret":"36b3bddb45f177575f63511b54c9e655" 
            },
            "env":{
                "正式环境":{
                    "http":"http://gw.api.taobao.com/router/rest",
                    "https":"https://eco.taobao.com/router/rest"
                },
                "测试环境":{
                    "http":"http://gw.api.tbsandbox.com/router/rest",
                    "https":"https://gw.api.tbsandbox.com/router/rest"
                },
                "protocol":"http",
                "sandbox":"正式环境"
            }},
            req_config=json.loads('''{
        "requestParams": [{
            "name": "fields",
            "value": "num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick",
            "description": "需返回的字段列表",
            "required": true
        }, {
            "name": "q",
            "value": "女装",
            "description": "查询词",
            "required": false
        }, {
            "name": "cat",
            "value": "16,18",
            "description": "后台类目ID，用,分割，最大10个，该ID可以通过taobao.itemcats.get接口获取到",
            "required": false
        }, {
            "name": "itemloc",
            "value": "杭州",
            "description": "所在地",
            "required": false
        }, {
            "name": "sort",
            "value": "tk_rate_des",
            "description": "排序_des（降序），排序_asc（升序），销量（total_sales），淘客佣金比率（tk_rate）， 累计推广量（tk_total_sales），总支出佣金（tk_total_commi）",
            "required": false
        }, {
            "name": "is_tmall",
            "value": "false",
            "description": "是否商城商品，设置为true表示该商品是属于淘宝商城商品，设置为false或不设置表示不判断这个属性",
            "required": false
        }, {
            "name": "is_overseas",
            "value": "false",
            "description": "是否海外商品，设置为true表示该商品是属于海外商品，设置为false或不设置表示不判断这个属性",
            "required": false
        }, {
            "name": "start_price",
            "value": "10",
            "description": "折扣价范围下限，单位：元",
            "required": false
        }, {
            "name": "end_price",
            "value": "10",
            "description": "折扣价范围上限，单位：元",
            "required": false
        }, {
            "name": "start_tk_rate",
            "value": "123",
            "description": "淘客佣金比率上限，如：1234表示12.34%",
            "required": false
        }, {
            "name": "end_tk_rate",
            "value": "123",
            "description": "淘客佣金比率下限，如：1234表示12.34%",
            "required": false
        }, {
            "name": "platform",
            "value": "1",
            "description": "链接形式：1：PC，2：无线，默认：１",
            "required": false
        }, {
            "name": "page_no",
            "value": "123",
            "description": "第几页，默认：１",
            "required": false
        }, {
            "name": "page_size",
            "value": "20",
            "description": "页大小，默认20，1~100",
            "required": false
        }],
        "description": "淘宝客商品查询",
        "name": "taobao.tbk.item.get"
    }'''),name='淘宝客商品查询')
    res = tb(fields="num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick",q="女装",cat='16,18')
    print(res)
