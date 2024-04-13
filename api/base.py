from loguru import logger
from typing import Any, Union, TypedDict, Tuple, Dict
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from collections import OrderedDict
from pathlib import Path
from subprocess import Popen, PIPE 
import re
import random
import sys
import os

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
    work_dir: Path

    def __init__(self) -> None:
        super().__init__()

        self.work_dir = Path(os.getcwd())
        self.logger = logger
        level = 'DEBUG' if self.debug else 'INFO'
        self.logger.add(sys.stderr, format=self.log_formatter, level=level)
        self.hooks = {'response': [self.log_respose]}
        self.headers = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Sec-Fetch-Dest': 'script',
            # 'Sec-Fetch-Mode': 'no-cors',
            # 'Sec-Fetch-Site': 'same-site',
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
        
        for cookieItem in cookieList:
            if len(cookieItem) < 2:
                self.logger.error(f'{cookieItem}的长度小于2')
                continue

            cookieName,cookieValue = cookieItem
            self.cookies.set(cookieName, cookieValue, domain=domain, path='/')
            logger.debug(f'加载cookie:{cookieItem}')
    
    def generate_random_str(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def typeStr(self, data: Any):
        if isinstance(data, int):
            return 'int'
        elif isinstance(data, float):
            return 'int'
        elif isinstance(data, bool):
            return 'bool'
        elif isinstance(data, list):
            return 'List[Any]'
        elif isinstance(data, dict):
            return 'Dict[str, Any]'
        return 'str'
    
    def runCmd(self, command: str):
        try:
            process = Popen(command, shell=True, cwd=self.work_dir, encoding='utf-8', stdout=PIPE)
            out, err = process.communicate()
            out = out.strip()
            return out

        except TimeoutError as err:
            print(err)
