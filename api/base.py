from loguru import logger
from typing import Any, Union, TypedDict, Tuple, Dict
import sys
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from collections import OrderedDict
import re

class ResponseKw(TypedDict):
    timeout: Union[int, None]
    proxies: OrderedDict
    stream: bool
    verify: bool
    cert: Union[Any, None]

class Base(Session):

    debug = False
    '''调试模式'''
    log_filename = 'log.txt'
    log_formatter = '{time} {level} {message}'
    '''日志文件名'''
    proxies = {}
    '''代理配置'''
    timeout = 20
    '''超时秒数'''

    def __init__(self) -> None:
        super().__init__()

        self.logger = logger
        level = 'DEBUG' if self.debug else 'INFO'
        self.logger.add(sys.stderr, format=self.log_formatter, level=level)
        self.hooks = {'response': self.log_respose}
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
    
    def log_request(self,request: Any):
        '''记录请求'''
        self.logger.debug('请求:', request)
    
    def log_respose(self, response: Response, *args: Tuple, **kwargs: ResponseKw):
        '''记录返回'''
        self.logger.debug('返回:{rtext}', rtext=response.text)
    
    def loadCookieStr(self, cookieStr: str, domain:str = ''):
        '''将从浏览器获取到cookie字符串转成字典'''
        ls = cookieStr.strip(';').replace(' ','').split(';')
        cookieList = [re.split(r'=',cookie,1) for cookie in ls]
        for cookieName,cookieValue in cookieList:
            self.cookies.set(cookieName, cookieValue, domain=domain)
