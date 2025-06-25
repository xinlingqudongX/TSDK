from ..types import taobao, eleme
from ..base import Base
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qsl, quote
from typing import Any, Dict, List
import json
from collections import OrderedDict
import time
import random
import hashlib
import datetime

class ElemeH5(Base):

    func_template: str
    appKey: str = '12574478'
    secret: str = ''
    platform: str = ''
    sandbox: bool = False
    domain: str = 'https://waimai-guide.ele.me'

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
    
    def onekeylogin(self):
        res = self.post('https://www.cmpassport.com/h5/onekeylogin/getNewTelecomPhonescrip?_bx-v=2.5.3',json={
            'businessType': '8',
            'encrypted': '',
            'reqdata': '',
        })
    @property
    def h5_token(self):
        token = self.cookies.get('_m_h5_tk', domain='', default='')
        if not token is None and len(token) > 32:
            return token[0:32]
        
        self.logger.error('从cookie获取的token为空')
        return ''

    @property
    def umidToken(self):
        '''获取umidToken'''
        return 'C' + str(int(time.time() * 1000)) + \
            ''.join(str(random.choice(range(10))) for _ in range(11)) + \
            str(int(time.time() * 1000)) +  \
            ''.join(str(random.choice(range(10))) for _ in range(3))

    def sign(self, token: str, t: str, appkey: str, data: str, binary: bool = False):
        """通过execjs执行test.js中的test函数生成签名"""
        try:
            import execjs
        except ImportError:
            raise ImportError("请先安装 execjs: pip install PyExecJS")
        import os
        js_path = os.path.join(os.path.dirname(__file__), './script.js')
        js_path = os.path.abspath(js_path)
        with open(js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        sign_str = f'{token}&{t}&{appkey}&{data}'
        self.logger.debug('sign签名字符串:{signStr}', signStr=sign_str)
        return ctx.call('sign', sign_str)

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
        appKey = payload.get('appKey', self.appKey)
        payload.update({
            't': timestamp,
            'type': 'json',
            'dataType': 'json',
        })
        payloadData = payload.get('data', {})
        dataStr = json.dumps(payloadData, separators=(',', ':'))
        payload.update({
            'sign': self.sign(self.h5_token, timestamp, appKey, dataStr),
            'data': dataStr
        })
        self.logger.debug('{method}请求:{payload}', payload=payload, method=method.upper())
        res = self.request(**request_options)
        resj: taobao.ApiRes = res.json()

        if res.status_code != 200:
            self.logger.error('API请求失败:{rtxt}', rtxt=res.text)
        else:
            ret = resj.get('ret')
            retMsg = ret[0]
            if 'SUCCESS' not in retMsg.upper():
                self.logger.error('API请求失败:{ret}', ret=ret)

        return (resj, res)
    
    def render_template(self, kwargs: Any):
        return self.func_template.format(**kwargs)
    
    def urlCreateFunc(self, api: str, method: str = 'get', func_name: str | None = None, desc: str = '', formdata: Any = {}):
        '''解析API链接为函数'''
        urlObj = urlparse(api)
        
        queryParams = dict(parse_qsl(urlObj.query))
        [platform, service_name, version, *SV] = urlObj.path.strip('/').split('/')

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
    
    def searchPoiNearby(self, keyword: str, latitude: float, longitue: float, offset: int = 0, limit: int = 20):
        '''搜索附近地址'''
        url = 'https://h5.ele.me/restapi/bgs/poi/search_poi_nearby'
        res = self.get(url, params={
            'keyword': quote(keyword),
            'offset': offset,
            'limit': limit,
            'latitude': latitude,
            'longitude': longitue,
        })
        resj: List[eleme.SearchPoiNearbyRes] = res.json()
        return resj

    def reverseGeoCoding(self, longitude: float, latitude: float):
        '''重新定位'''
        url = 'https://h5.ele.me/restapi/bgs/poi/reverse_geo_coding'
        res = self.get(url,params={
            'latitude': latitude,
            'longitude': longitude
        })
        resj: eleme.reverseGeoCodingRes = res.json()
        return resj


    def MtopVenusShopresourceserviceGetshopresource(self, data: Any = {}):
        """mtop.venus.shopresourceservice.getshopresource函数"""

        method = 'get'
        params = {'jsv': '2.7.1', 'appKey': '12574478', 't': '1701086935133', 'sign': '21f5d98752b48dcb5e1a2d59eacb6529', 'api': 'mtop.venus.ShopResourceService.getShopResource', 'v': '1.4', 'type': 'originaljson', 'dataType': 'json', 'ecode': '1', 'SV': '5.0', 'data': {'lat': 30.452488, 'lng': 114.319347, 'from': 'native', 'bizChannel': 'mobile.default.default', 'deviceId': '500B511F28CE4C29996AC6EC4EDCA549|1701086828893', 'livingShowChannel': 'other', 'channel': 'PC', 'subChannel': 'ELE_APP', 'store_id': '1102570163', 'ele_id': 'E14249670395629855804', 'itemId': '', 'scentExtend': '{"businessComeFrom":""}'}, 'bx_et': 'dxvJc1wTGq0k4LyJbzhmY30xbsomsLKrMU-_KwbuOELvzGCBZemyMpLGu6AuE62dAeYRKa6hFwZplH1WK07hpvLVueCE4wbCJexBZmDiI3-PL9_KSADgxFBFd8rH-Jxy49WQmyGMG3yp7A4VU9PjobZ_QdJhVfI_sbXxGKsRwNehkJeKxgCR53_YurWNfdvOWeaGWMVSDmFUT_sqdoAHc'}
        url = 'https://waimai-guide.ele.me/h5/mtop.venus.shopresourceservice.getshopresource/1.4/5.0/'
        if data:
            params['data'].update(data)

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        if method.upper() == 'GET':
            request_options.setdefault('params', params)
        else:
            request_options.setdefault('data', params)

        return self._execute(request_options)

    def MtopAlscWamaiStoreDetailBusinessTabPhone(self, data: Any = {}):
        """mtop.alsc.wamai.store.detail.business.tab.phone函数"""

        method = 'POST'
        params = {'jsv': '2.7.2', 'appKey': '12574478', 't': '1701088333698', 'sign': '630d4b8b2f0a555bb22462fb62b990be', 'api': 'mtop.alsc.wamai.store.detail.business.tab.phone', 'v': '1.0', 'type': 'originaljson', 'dataType': 'json', 'timeout': '10000', 'mainDomain': 'ele.me', 'subDomain': 'waimai-guide', 'H5Request': 'true', 'ttid': 'h5@chrome_pc_119.0.0.0', 'SV': '5.0', 'bx_et': 'dBlwr-v97CdZ1VE6eRV4ao-HpLVTs7KWmjZboq005lqiGPDFgDnznRTTsJ03urr0mR2G-64zyPq0jPmEomi-C1NMWE54A4YT1FF1irqIb-GXWsiFgDnzIsGqkszmomLTcFpIWVFYi3t7gQgtWkGeV36by_Z7MSxWVmE0B6Vx4jNrWGh4FNXFT-xoykcnKB6MDaqYYsfPyPyMlV6fZ_X0SREuRkWZyiUhvhlxQiX4IyUUVe8UdPQ83'}
        url = 'https://waimai-guide.ele.me/h5/mtop.alsc.wamai.store.detail.business.tab.phone/1.0/5.0/'
        payload = params.get('data', {'eleStoreId': 'E6480404258831972301'})
        if data:
            payload.update(data)

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        request_options.setdefault('params', params)
        if method.upper() == 'POST':
            request_options.setdefault('data', payload)

        return self._execute(request_options)

    def MtopAlscUserSessionEleCheck(self, data: Any = {}):
        """mtop.alsc.user.session.ele.check函数"""

        method = 'get'
        params = {'jsv': '2.7.5', 'appKey': '12574478', 't': '1750813282236', 'sign': 'b11f35a93b31d469eaaf13223ff3f692', 'api': 'mtop.alsc.user.session.ele.check', 'v': '1.0', 'type': 'originaljson', 'dataType': 'json', 'timeout': '5000', 'mainDomain': 'ele.me', 'subDomain': 'waimai-guide', 'pageDomain': 'ele.me', 'H5Request': 'true', 'syncCookieMode': 'true'}
        url = 'https://waimai-guide.ele.me/h5/mtop.alsc.user.session.ele.check/1.0/'
        payload = params.get('data', {})
        if data:
            payload.update(data)

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        request_options.setdefault('params', params)
        if method.upper() == 'POST':
            request_options.setdefault('data', payload)

        return self._execute(request_options)
