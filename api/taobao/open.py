from ..types import taobao
from ..base import Base
from collections import OrderedDict
from typing import Any, List, Dict, TypedDict, Union, Optional
import json
import hashlib
import hmac
import datetime

class ApiDefaultParams(TypedDict):
    method: str
    app_key: str
    session: Optional[str]
    timestamp: str
    v: str
    sign_method: str
    sign: str
    format: str

class ApiParams(TypedDict):
    method: str
    data: Any

class TaobaoOpen(Base):

    appKey: str
    appSecret: str
    signMethod: str
    version: str
    apiUrl: str = 'https://eco.taobao.com/router/rest'

    def __init__(self, appKey: str, appSecret: str) -> None:
        super().__init__()
        self.appKey = appKey
        self.appSecret = appSecret

        self.defaultParams: ApiDefaultParams = {
            'method': '',
            'session': '',
            'app_key': self.appKey,
            'sign_method': 'md5',
            'timestamp':'2016-01-01 12:00:00',
            'v': '2.0',
            'format': 'json',
            'sign': ''
        }
    
    def hmacSign(self, appSecret: str, data: Any, binary: bool = False) -> str:
        keys = list(filter(lambda key: data[key], data))
        sortKey = sorted(keys, key=lambda x:x)
        sign_str = ''.join(list(map(lambda key: ''.join([key, data[key]]), sortKey)))
        self.logger.debug('hmac签名字符串:{sign_str}',sign_str=sign_str)
        func = 'digest' if binary else 'hexdigest'
        return getattr(hmac.HMAC(appSecret.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256),func)().upper()

    def md5Sign(self, appSecret: str, data: Any, binary: bool = False) -> str:
        keys = list(filter(lambda key: data[key], data))
        sortKey = sorted(keys, key=lambda x:x)
        sign_str = ''.join(list(map(lambda key: ''.join([key, data[key]]), sortKey)))
        self.logger.debug('md5签名字符串:{sign_str}',sign_str=sign_str)
        func = 'digest' if binary else 'hexdigest'
        return getattr(hashlib.md5(f'{appSecret}{sign_str}{appSecret}'.encode('utf-8')),func)().upper()

    def _execute(self, api: str, data: Dict):
        options = {}
        copyDefault = OrderedDict(self.defaultParams)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        # timestamp = '2016-01-01 12:00:00'
        signData = {**self.defaultParams, **data, 'method': api, 'timestamp': timestamp}
        sign = self.md5Sign(self.appSecret, signData)
        
        copyDefault.update({
            'method': api,
            'timestamp': timestamp,
            'sign': sign,
            **data
        })
        keys = list(copyDefault.keys())
        for key in keys:
            val = copyDefault[key]
            if type(val) is bool and not val:
                copyDefault.pop(key)
            elif type(val) is str and not val:
                copyDefault.pop(key)
            else:
                pass

        options.update({
            'method': 'post',
            'url': self.apiUrl,
            'params': copyDefault,
            'proxies': {
                'http': {},
                'https': {}
            },
        })

        self.logger.debug('请求的参数:{options}', options=options)
        res = self.request(**options)
        if res.status_code != 200:
            self.logger.error('请求错误:{rtxt}',rtxt=res.text)

        resj: taobao.OpenApiRes = res.json()
        errRes = resj.get('error_response')
        if errRes:
            self.logger.error('请求失败:{errRes}', errRes=errRes)
            self.logger.error('请求链接:{rurl}', rurl=res.url)

        return resj
    
    def reort(self):
        data = self._execute('taobao.tbk.dg.vegas.send.report', {
            "biz_date": "20210101",
            "activity_id": "1462",
        })
