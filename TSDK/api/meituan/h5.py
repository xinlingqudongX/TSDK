from ..types import taobao
from ..base import Base
from typing import Any, List
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qsl
from typing import Any, Dict, List
import json
from collections import OrderedDict
import time
import random
import hashlib
import datetime

class MeituanH5(Base):

    domain: str = 'https://i.waimai.meituan.com'
    wm_latitude: int
    wm_longitude: int

    def __init__(self) -> None:
        super().__init__()

        self.func_template = '''
    def {func_name}(self, data: Any = {{}}):
        """{desc}"""

        method = '{method}'
        params = {payload}
        url = '{scheme}://{hostname}{path}'
        payload = params.get('data', {formdata})
        if data:
            payload.update(data)

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        request_options.setdefault('params', params)
        if method.upper() == 'POST':
            request_options.setdefault('data', payload)

        return self._execute(request_options)
'''
        self.headers.update({
            'Host': 'i.waimai.meituan.com',
            'Origin':'https://h5.waimai.meituan.com',
            'Referer': 'https://h5.waimai.meituan.com/',
            'Mtgsig': '{"a1":"1.1","a2":1701171239880,"a3":"76wv10zu717951621w6v5uy5xy8y1uuu81x84y5182y97958u9901wu5","a5":"4TOOlGFeVKPK0hSzihlN9MXi9lL6R/UGsZ==","a6":"h1.5oTrO+xVvWOVJm25gTqVKesIDkVsvwJMx9slKCLGpCdJpyg3S0SchOL5xUITTGZ7+NhCenCO9mU7tbfr5k9wzpmjt6aFw4HaZYUaq8jGSU3LQXhkEADZ211HDbIcS6DBut1V6Zzn1CI1yywQ3xNPcyR8sVDzDleEKxILHV/WcZnuJiRBzhOrQpSWwH9tNRipnZzZ4TrchZTTDluZLeNKacURF3JlQ2W85rd4qQ0UbCfNKAQr6N/HkaGswAGoKCRJqAl3n8u8WIxEbr2bpaMQmR3Rv+DTsVmUUia1D/I0h2mRi4KDnrjupsMY89NRnORTXnrYyAc0E5eois6t0EwUTpLfRUl/yJX9634tAttuTQJHe3iEsZUHE0nmTJZAibVCVl4iZwX3CJ0e2WAYFdDRHzxuV0uSa+fHNltEKjulPnl0=","x0":4,"d1":"e272a265fe77afb9422b8a351c050dc2"}'
        })
    
    @property
    def uuid(self):
        token = self.cookies.get('uuid', domain='', default='')
        if not token is None and len(token) > 32:
            return token[0:32]
        
        self.logger.error('从cookie获取的token为空')
        return ''
    
    @property
    def openh5_uuid(self):
        token = self.cookies.get('uuid', domain='', default='')
        if not token is None and len(token) > 32:
            return token[0:32]
        
        self.logger.error('从cookie获取的token为空')
        return ''

    def render_template(self, kwargs: Any):
        return self.func_template.format(**kwargs)
    
    def urlCreateFunc(self, api: str, method: str = 'get', func_name: str | None = None, desc: str = '', formdata: Any = {}):
        '''解析API链接为函数'''
        urlObj = urlparse(api)
        
        queryParams = dict(parse_qsl(urlObj.query))
        [env, platform, service_name, version, SV] = urlObj.path.strip('/').split('/')

        func_name = func_name if func_name else ''.join([i.capitalize() for i in service_name.split('.')])
        if hasattr(self, func_name):
            return
        
        for key in queryParams:
            val = queryParams[key]
            if len(re.findall(r'\{.*?\}|\[.*?\]', val)) > 0:
                queryParams[key] = json.loads(val)
        
        with open(__file__, 'a+', encoding='utf-8') as f:
            funcStr = self.render_template({
                'payload': queryParams,
                'hostname': urlObj.hostname,
                'scheme': urlObj.scheme,
                'path': urlObj.path,
                'params': urlObj.params,
                'func_name': func_name,
                'service_name': service_name,
                'platform': platform,
                'version': version,
                'desc': desc if desc else f'{service_name}函数',
                'method': method,
                'formdata': formdata,
            })
            f.write(funcStr)
    
    def createTypes(self, typeName: str, data: Dict[str, Any]):
        '''创建类型'''
        if not data:
            return
        
        formatter = '''

class {typeName}(TypedDict):
{fieldStr}
'''
        fieldStr = ''
        for key in data:
            val = data[key]
            if type(val) is str:
                fieldStr += f'    {key}: str\n'
            elif type(val) is list:
                fieldStr += f'    {key}: List'
            elif type(val) is dict:
                fieldStr += f'    {key}: Dict'
            elif type(val) is int:
                fieldStr += f'    {key}: int'
            elif type(val) is float:
                fieldStr += f'    {key}: float'
            elif type(val) is bool:
                fieldStr += f'    {key}: bool'
            else:
                fieldStr += f'    {key}: Any'
        
        nowFile = Path(__file__)
        typeFile = nowFile.parent.parent.joinpath('types/taobao.py')
        with open(typeFile, 'a+', encoding='utf-8') as f:
            typeStr = formatter.format(**{
                'typeName': typeName,
                'fieldStr': fieldStr,
            })
            f.write(typeStr)

    def _execute(self, request_options: Any):
        '''解析请求参数并将参数进行加密'''
        method = request_options.get('method')
        if method.upper() == 'GET':
            payload = request_options.get('params')
        else:
            payload = request_options.get('data')
        
        if payload is None:
            raise Exception('提交的数据不能为None')
        
        timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
        payload.update({
            't': timestamp,
            'type': 'json',
            'dataType': 'json',
        })
        payloadData = payload.get('data', {})
        dataStr = json.dumps(payloadData, separators=(',', ':'))
        self.logger.debug('{method}请求:{payload}', payload=payload, method=method.upper())
        res = self.request(**request_options)
        if res.status_code != 200:
            self.logger.error('API请求失败:{rtxt}', rtxt=res.text)
            return None
        else:
            resj: taobao.ApiRes = res.json()
            ret = resj.get('ret')
            retMsg = ret[0]
            if 'SUCCESS' not in retMsg.upper():
                self.logger.error('API请求失败:{ret}', ret=ret)

        return (resj, res)


    def Openh5(self, data: Any = {}):
        """openh5函数"""

        method = 'POST'
        params = {'_': '1701171239879', 'yodaReady': 'h5', 'csecplatform': '4', 'csecversion': '2.3.1'}
        url = 'https://i.waimai.meituan.com/tsp/open/openh5/home/shopList'
        payload = params.get('data', {'ptimus_code': '10', 'optimus_risk_level': '71', 'pageSize': '20', 'page_index': '0', 'offset': '0', 'content_personalized_switch': '0', 'sort_type': '', 'slider_select_data': '', 'activity_filter_codes': '', 'wm_latitude': '30491030', 'wm_longitude': '114403269', 'wmUuidDeregistration': '0', 'wmUserIdDeregistration': '0', 'openh5_uuid': '787A54B7E94A85955D1ABD26FA46CD68A3351FC0428B8882195DC25ABFF6C502', 'uuid': '787A54B7E94A85955D1ABD26FA46CD68A3351FC0428B8882195DC25ABFF6C502'})
        if data:
            payload.update(data)

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        request_options.setdefault('params', params)
        if method.upper() == 'POST':
            request_options.setdefault('data', payload)

        return self._execute(request_options)
