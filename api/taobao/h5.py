from urllib.parse import urlparse, parse_qsl, quote
from typing import TypedDict, List, Dict, Any
from collections import OrderedDict
from pathlib import Path
from PIL import Image
from io import BytesIO
import hashlib
import datetime
import json
import time
import random
import re
from ..types import taobao
from ..base import Base

class RequestOptions(TypedDict):
    method: str
    url: str
    data: Dict[str, Any]
    params: Dict[str, Any]

class TaobaoH5(Base):

    func_template: str
    appKey: str = '12574478'
    secret: str = ''
    platform: str = ''
    sandbox: bool = False
    domain: str = 'https://www.taobao.com'
    whiteCookieNames = [
        'cookie2',
        '_tb_token_',
        'unb',
        'cookie17',
        '_cc_',
        '_l_g_',
        'sg',
        'cookie1',
        '_m_h5_tk',
        '_m_h5_tk_enc',
    ]
    createTypesFile: bool = False

    def __init__(self) -> None:
        super().__init__()
        
        self.func_template = '''
    def {func_name}(self, data: Any = {}):
        """{desc}"""

        method = '{method}'
        params = {payload}
        url = '{scheme}://{hostname}{path}'
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
''' 
        self.initCookie()

    def initCookie(self):
        '''初始化cookie'''
        _uab_collina = ''
        for _ in range(20):
            if len(_uab_collina) < 11:
                _uab_collina += str(random.random())[2:]
            else:
                break
        #第一个cookie,domain为login.taobao.com，path为/member
        _uab_collina = str(int(time.time() * 1000)) + _uab_collina[len(_uab_collina) - 11:]
        self.cookies.set('_uab_collina',_uab_collina,domain='login.taobao.com',path='/member')

        #第二个cookie，请求这个JS，https://log.mmstat.com/eg.js，然后把etag的值设置为cna
        res = self.get('https://log.mmstat.com/eg.js')
        cna = re.findall(r'Etag="(.*?)"',res.text)[0]
        self.cookies.set('cna',cna,domain='.taobao.com',path='/')

        #第三个cookie，isg为算法生成的，不好破解，domain为.taobao.com，path为/
        isg = 'BM3NGuFcrQh-tgkk_KLDk9jr3OlHqgF8pnooOQ9SCWTTBu241_oRTBuUcNrFxhk0'
        self.cookies.set('isg',isg,domain='.taobao.com',path='/')

        #第四个cookie，l为算法生成,domain为.taobao.com，path为/
        l = 'bBgKwFjlv-QtIl3JBOCanurza77OSIRYYuPzaNbMi_5pK6T_Bk7OlgnjDF96Vj5RsxYB4-L8Y1J9-etkZ'
        self.cookies.set('l',l,domain='.taobao.com',path='/')

        self.get('https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478')

    def clearCookie(self):
        for key in self.cookies.iterkeys():
            if key not in self.whiteCookieNames:
                self.cookies.set(key, None)

    @property
    def h5_token(self):
        token = self.cookies.get('_m_h5_tk', domain='.taobao.com', default='')
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
        '''sign签名加密方式采用淘宝H5网页的加密流程
        data传递使用的是字符串，一是为了少加密一次，二是为了直接说明这个要转成json字符串，还需要去掉空格'''

        sign_func = 'digest' if binary else 'hexdigest'
        sign_str = f'{token}&{t}&{appkey}&{data}'
        self.logger.debug('sign签名字符串:{signStr}',signStr=sign_str)
        return getattr(hashlib.md5(sign_str.encode('utf-8')),sign_func)()

    
    def render_template(self, kwargs: Any):
        return self.func_template.format(**kwargs)
    
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
            self.logger.error('API请求失败:{api}', res.text)
        else:
            ret = resj.get('ret')
            retMsg = ret[0]
            if 'SUCCESS' not in retMsg.upper():
                self.logger.error('API请求失败:{ret}', ret=ret)

        return (resj, res)

    def qrLogin(self, timeout: int = 60) -> bool:
        '''二维码登录'''
        umidToken = self.umidToken
        res = self.get(f'https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.754894437.1.5af92a89ix8uWh&f=top&redirectURL={quote(self.domain)}')
        if res.status_code != 200:
            self.logger.error('初始化cooie失败，请检查原因:',res.text)
            return False
        res = self.get(f'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={umidToken}')
        resj: taobao.QrLoginRes = res.json()
        lgToken = resj.get('lgToken')
        qrcodeUrl = resj.get('url')
        imgRes = self.get(f'https:{qrcodeUrl}')
        if imgRes.status_code != 200:
            self.logger.error('获取登录二维码失败:{rtxt}', rtxt=res.text)
            return False
        img = Image.open(BytesIO(imgRes.content))
        img.show()

        while timeout > 0:
            checkRes = self.qrCheck(lgToken, umidToken)
            checkCode = checkRes.get('code')
            if checkCode == taobao.QrStateCode.扫码成功.value:
                checkUrl = checkRes.get('url') + '&umid_token=' + umidToken
                mainRes = self.get(checkUrl)
                if mainRes.url.find('login_unusual.htm') > -1:
                    [judgeTrueHref,judgeFalseHref, safeHref, nosafeHref] = re.findall(r'window\.location\.href = "(.*?)"',mainRes.text)
                    safeRes = self.get(safeHref)
                    self.logger.debug('安全登录跳转返回:{tt}', tt=safeRes.text)

                    data, res = self.getUserSimple()
                    if not data.get('data'):
                        self.logger.error('需要安全验证登录:{rtext}', rtext=mainRes.text)
                        break
                return True
            elif checkCode == taobao.QrStateCode.二维码过期.value:
                self.logger.debug('二维码过期: {res}', res=checkRes)
                break
            else:
                pass
            
            timeout -= 1
            time.sleep(1)
        
        img.close()
        return False
    
    def qrCheck(self, lgToken: str, umidToken: str):
        self.headers.update({
            'Referer':'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=&popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str=&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang=zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75sOSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKMe0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwALGnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'
        })
        res = self.get(f'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={lgToken}&defaulturl=www.taobao.com')
        resj: taobao.QrStateRes = res.json()
        self.logger.debug('检查qrcode登录状态:{resj}', resj=resj)
        return resj

    def urlCreateFunc(self, api: str, method: str = 'get', func_name: str | None = None, desc: str = ''):
        '''解析API链接为函数'''
        urlObj = urlparse(api)
        
        queryParams = dict(parse_qsl(urlObj.query))
        [platform, service_name, version] = urlObj.path.strip('/').split('/')

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

    def getUserSimple(self):
        """mtop.user.getusersimple函数"""

        method = 'get'
        params = {
            'jsv': '2.6.1', 
            'appKey': '12574478', 
            't': '1700983359826', 
            'sign': '8b00a80f1fded8662d00ae20d9b3d81c', 
            'api': 'mtop.user.getUserSimple', 
            'v': '1.0', 
            'ecode': '1', 
            'sessionOption': 'AutoLoginOnly', 
            'jsonpIncPrefix': 'liblogin', 
            'type': 'json', 
            'dataType': 'json', 
            'callback': 'mtopjsonpliblogin4', 
            'data': {}
        }
        url = 'https://h5api.m.taobao.com/h5/mtop.user.getusersimple/1.0/'

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        if method.upper() == 'GET':
            request_options.setdefault('params', params)
        else:
            request_options.setdefault('data', params)

        return self._execute(request_options)
