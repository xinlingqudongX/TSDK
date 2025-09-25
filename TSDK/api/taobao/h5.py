from urllib.parse import urlparse, parse_qsl, quote
from typing import TypedDict, List, Dict, Any
from collections import OrderedDict
from pathlib import Path
from requests import Response
from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import Response as PlayResponse
from playwright.sync_api import Request as PlayRequest
from json import JSONDecodeError
from ..types import taobao
from ..base import Base
import hashlib
import datetime
import json
import time
import random
import re
import os
import qrcode


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
        'sgcookie',
        #   验证码通过后的cookie
        'x5sec',
    ]
    createTypesFile: bool = False
    _login_csrf: str = ''
    _login_umidtoken: str = ''
    
    fail_ret_status = {
        'FAIL_SYS_USER_VALIDATE': ''
    }

    def __init__(self) -> None:
        super().__init__()
        self.verify = False
        self.login_url = 'https://login.m.taobao.com/mlogin/login.htm'
        
        self.func_template = '''
    def {func_name}(self, data: Any = {{}}):
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

        # #第三个cookie，isg为算法生成的，不好破解，domain为.taobao.com，path为/
        # isg = 'BM3NGuFcrQh-tgkk_KLDk9jr3OlHqgF8pnooOQ9SCWTTBu241_oRTBuUcNrFxhk0'
        # self.cookies.set('isg',isg,domain='.taobao.com',path='/')

        # #第四个cookie，l为算法生成,domain为.taobao.com，path为/
        # l = 'bBgKwFjlv-QtIl3JBOCanurza77OSIRYYuPzaNbMi_5pK6T_Bk7OlgnjDF96Vj5RsxYB4-L8Y1J9-etkZ'
        # self.cookies.set('l',l,domain='.taobao.com',path='/')

        #   初始化_tb_token,cookie2,t等cookie
        self.get('https://h5api.m.taobao.com/h5/mtop.user.getusersimple/1.0/')
        self.get('https://h5api.m.taobao.com/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478')
        self.cookies.set('thw','cn', domain='.taobao.com',path='/')
        self.cookies.set('xlly_s','1', domain='.taobao.com',path='/')
        self.cookies.set('_samesite_flag_','true', domain='.taobao.com',path='/')

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
    def deviceId(self):
        return self.cookies.get('cna', domain='.taobao.com', default='')

    @property
    def hsiz(self):
        token = self.cookies.get('cookie2', domain='.taobao.com', default='')
        if not token is None and len(token) > 0:
            return token
        
        self.logger.error('从cookie获取的hsiz为空')
        return ''

    @property
    def umidToken(self):
        '''获取umidToken'''
        return self._login_umidtoken
        # return 'C' + str(int(time.time() * 1000)) + \
        #     ''.join(str(random.choice(range(10))) for _ in range(11)) + \
        #     str(int(time.time() * 1000)) +  \
        #     ''.join(str(random.choice(range(10))) for _ in range(3))
    
    @property
    def loginCsrfToken(self):
        return self._login_csrf

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
            'callback': '',
        })
        payloadData = payload.get('data', {})
        dataStr = json.dumps(payloadData, separators=(',', ':'))
        payload.update({
            'sign': self.sign(self.h5_token, timestamp, appKey, dataStr),
            'data': dataStr
        })
        self.logger.debug('{method}请求:{payload}', payload=payload, method=method.upper())
        # self.headers.update({
        #     'Referer': 'https://h5.m.taobao.com'
        # })
        res = self.request(**request_options)
        try:
            resj: taobao.ApiRes = res.json()
            if res.status_code != 200:
                self.logger.error('API请求失败:{api}', res.text)
            else:
                ret = resj.get('ret')
                if not any(filter(lambda retStatus: 'SUCCESS' in retStatus, ret)):
                    self.logger.error('API请求失败:{ret}', ret=ret)
                    if len(ret) >= 2:
                        retStatus, retMsg, *_ = ret
                    
                        if retStatus in self.fail_ret_status:
                            jumpUrl = resj.get('data', {}).get('url')
                            if jumpUrl:
                                self.__hookX5(res, jumpUrl)

            return (resj, res)
        except JSONDecodeError as err:
            self.__hookX5(res)
            return {}, res
            
        except Exception as err:
            self.logger.error('请求错误：{err}', err=err)
            return {}, res
    def _login_bofore(self):
        res = self.get(f'https://login.taobao.com/havanaone/login/login.htm?bizName=taobao&f=top&redirectURL={quote(self.domain)}')
        if res.status_code != 200:
            self.logger.error('初始化cooie失败，请检查原因:',res.text)
            return False
        # 提取csrf
        regex = re.findall(r'viewData = (\{.*\})',res.text)
        if len(regex) <= 0:
            self.logger.error('提取csrf失败')
        viewData: taobao.LoginViewData2 = json.loads(regex[0])
        loginForm = viewData.get('loginFormData')
        self._login_csrf = loginForm.get('_csrf')
        self._login_umidtoken = loginForm.get('umidToken')

    def qrLogin(self, timeout: int = 60, autoTrust: bool = False) -> bool:
        '''二维码登录'''
        umidToken = self.umidToken
        self._login_bofore()

        res = self.get('https://login.taobao.com/havanaone/loginLegacy/qrCode/generate.do', params={
            'bizEntrance':'taobao_pc',
            'bizName':'taobao',
            'hitRSA2048Gray':'true',
            '_csrf': self.loginCsrfToken,
            'umidToken': self.umidToken,
            'lang': 'zh_CN',
            'returnUrl': self.domain,
            'umidTag': 'NOT_INIT',
            # 'bx-ua':'',
            # 'bx-umidtoken':'',
            # 'bx_et':'',
        })
        resj: taobao.QrLoginRes = res.json()
        t = resj.get('content').get('data').get('t')
        ck = resj.get('content').get('data').get('ck')
        qrUrl = resj.get('content').get('data').get('codeContent')
        # qrcode url:https://login.m.taobao.com/qrcodeCheck.htm?lgToken=c21f2d0128b033123fad100d609c51d4&tbScanOpenType=Notification
        qrcodeImg = qrcode.make(qrUrl)
        with open('qrcode.png','wb') as f:
            qrcodeImg.save(f)

        # if imgRes.status_code != 200:
        #     self.logger.error('获取登录二维码失败:{rtxt}', rtxt=res.text)
        #     return False
        os.system('start qrcode.png')

        while timeout > 0:
            checkData = self.qrNewCheck2(t, ck)
            qrCodeStatus = checkData.get('qrCodeStatus')
            if qrCodeStatus == taobao.QrStatus.已确认.value:
                self.logger.debug(f'已确认:{checkData}')
                imgUrls = checkData.get('asyncUrls')
                if imgUrls:
                    for url in imgUrls:
                        self.get(url)

                mainUrl = checkData.get('iframeRedirectUrl')
                if mainUrl:
                    self.get(mainUrl)
                #   获取h5token
                self.getUserSimple()
                # checkUrl = checkRes.get('url') + '&umid_token=' + umidToken
                # mainRes = self.get(checkUrl)
                # if mainRes.url.find('login_unusual.htm') > -1:
                #     [judgeTrueHref,judgeFalseHref, safeHref, nosafeHref] = re.findall(r'window\.location\.href = "(.*?)"',mainRes.text)
                #     safeRes = self.get(safeHref)
                #     self.logger.debug('安全登录跳转返回:{tt}', tt=safeRes.text)

                #     data, res = self.getUserSimple()
                #     if not data.get('data'):
                #         self.logger.error('需要安全验证登录:{rtext}', rtext=mainRes.text)
                #         break
                if autoTrust:
                    # 自动信任
                    self.trustDevice(ck, autoTrust)

                return True
            elif qrCodeStatus == taobao.QrStatus.已过期.value:
                self.logger.debug('二维码过期: {res}', res=checkData)
                break
            else:
                pass
            
            timeout -= 1
            time.sleep(1)
        
        return False
    
    def qrCheck(self, lgToken: str, umidToken: str):
        self.headers.update({
            'Referer':'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=&popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str=&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang=zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75sOSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKMe0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwALGnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'
        })
        res = self.get(f'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={lgToken}&defaulturl=www.taobao.com')
        resj: taobao.QrStateRes = res.json()
        self.logger.debug('检查qrcode登录状态:{resj}', resj=resj)
        return resj

    def qrNewCheck(self, t: int, ck: str, ):
        res = self.post('https://login.taobao.com/newlogin/qrcode/query.do?appName=taobao&fromSite=0', data={
            't': t,
            'ck': ck,
            'appName': 'taobao',
            'appEntrance': 'taobao_pc',
            '_csrf_token': self.loginCsrfToken,
            'umidToken': self.umidToken,
            'hsiz': self.hsiz,
            'newMini2': True,
            'bizParams':'',
            'full_redirect': False,
            'mainPage': False,
            'style': 'mini',
            'appkey': '00000000',
            'from':'sm',
            'isMobile': False,
            'umidTag': 'SERVER',
            'navUserAgent':'',
            'navPlatform': 'Win32',
            'isIframe': False,
            'defaultView':'qrcode',
            'deviceId': '',
            'pageTraceId':'',
        })
        resj = res.json()
        hasError = resj.get('hasError')
        if hasError:
            self.logger.error('请求错误:{resj}', resj=resj)
        self.logger.debug(f'检查返回:{resj}')
        resData:taobao.QrCheckData = resj.get('content',{}).get('data')
        return resData

    def qrNewCheck2(self, t: int, ck: str):
        res = self.post('https://login.taobao.com/havanaone/loginLegacy/qrCode/query.do?bizEntrance=taobao_pc&bizName=taobao', data={
            't': t,
            'ck': ck,
            'ua':'',
            'hitRSA2048Gray': True,
            'bizEntrance': 'taobao_pc',
            'bizName': 'taobao',
            'renderRefer': 'https://www.taobao.com/',
            '_csrf': self.loginCsrfToken,
            'lang':'zh_CN',
            'umidToken': self.umidToken,
            'umidTag': 'NOT_INIT',
            'navLanguage':'zh-CN',
            'navUserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'navPlatform':'Win32',
            'isIframe':'false',
            'banThirdPartyCookie':'true',
            'documentReferer':'https://www.taobao.com/',
            'defaultView':'password',
            'deviceId': self.deviceId,
        })
        resj = res.json()
        hasError = resj.get('hasError')
        if hasError:
            self.logger.error('请求错误:{resj}', resj=resj)
        self.logger.debug(f'检查返回:{resj}')
        resData:taobao.QrCheckData = resj.get('content',{}).get('data')
        return resData

    def sendSms(self, phone:str, country:str = 'CN', code = '86'):
        '''登录短信验证码发送'''
        self._login_bofore()

        res = self.post('https://login.m.taobao.com/havanaone/loginLegacy/recommendLoginFlow.do?bizEntrance=taobao_h5&bizName=taobao',data={
            'simBizType': 0,
            'loginId': phone,
            'phoneCode': code,
            'countryCode': country,
            'keepLogin': True,
            'contextToken':'',
            'defaultView': 'sim'
        })

        # 发送验证码
        res = self.post('https://login.m.taobao.com/havanaone/loginLegacy/sms/sendSms.do?bizEntrance=taobao_h5&bizName=taobao', data={
            'phoneCode': code,
            'loginId': phone,
            'countryCode': country,
            'contextToken':'',
            'defaultView': 'sim',
            '_csrf': self._login_csrf,
            'lang': 'zh_CN'
        })
        resj: taobao.SendSmsRes = res.json()
        smsData = resj.get('content').get('data')

        return smsData
        #   

    def loginSms(self,phone:str,smsCode:str, smsToken: str, country:str = 'CN', code = '86'):
        '''短信验证码登录'''
        res = self.post('https://login.m.taobao.com/havanaone/loginLegacy/sms/login.do?bizEntrance=taobao_h5&bizName=taobao', data={
            'loginId': phone,
            'phoneCode': code,
            'countryCode': country,
            'keepLogin': True,
            'contextToken':'',
            'smsCode': smsCode,
            'smsToken': smsToken
        })

        resj: taobao.LoginSmsRes = res.json()

        smsData = resj.get('content').get('data')
        redirectUrl = smsData.get('redirectUrl')
        if redirectUrl:
            self.get(redirectUrl)
        self.getUserSimple()
        
        return resj

    def trustDevice(self, ck: str, trust: bool):
        '''信任设备'''
        res = self.post('https://login.taobao.com/havanaone/login/autoLogin/choose.do',params={
            'token': ck.replace('qr_code_',''),
            'chooseNextAction': 'clearAutoLoginToken',
            'chooseButton': trust,
        }, json={
            'dialogStress': trust,
            'deviceId': self.deviceId,
        })

        resj: Any = res.json()
        return resj

    def __hookX5(self, res: Response, jumpUrl: str = ''):
        ufeResult = res.headers.get('ufe-result')
        x5PunishCache = res.headers.get('x5-punish-cache')
        bxpunish = res.headers.get('bxpunish')
        via = res.headers.get('via')
        bxuuid = res.headers.get('bxuuid')

        if not all([ufeResult, x5PunishCache, bxpunish, via]):
            return
        
        if not jumpUrl and 'x5referer' in res.text:
            locationHref = re.findall(r'href\s*=\s*"(.*?)"', res.text)
            if len(locationHref) <= 0:
                self.logger.error('提取跳转链接失败:{rtxt}',rtxt=res.text)
                return
            
            jumpUrl = locationHref[0] + quote(res.url)

        self.logger.debug('打开链接:{jumpUrl}', jumpUrl=jumpUrl)
        playwright = sync_playwright().start()
        iPhone13 = playwright.devices['iPhone 13']
        self.logger.debug('设备列表:{devices}',devices=playwright.devices)
        browser = playwright.chromium.launch(headless=False, devtools=self.debug)
        context = browser.new_context(
            **iPhone13,
            # is_mobile=False,
            # device_scale_factor=1.0,
            record_video_dir='video/',
        )
        cookie: List[Any] = [{ 'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path} for cookie in self.cookies]
        context.add_cookies(cookie)
        page = context.new_page()
        page.goto(jumpUrl)

        page.screenshot(path="example.png")

        self.__drag_element(page)
        browser.close()

        playwright.stop()
    
    def __drag_element(self, page: Page, elementSelector: str = '#nc_1_n1z'):
        element = page.locator(elementSelector)
        if not element:
            self.logger.error('未找到元素', elementSelector)
            return
        
        elementPos = element.bounding_box()
        if not elementPos:
            self.logger.error('获取位置出错')
            return
        
        target_pos = { 'x': elementPos['x'] + 300, 'y': elementPos['y']}

        element.hover()
        page.mouse.down()
        page.mouse.move(target_pos['x'], target_pos['y'])
        page.mouse.up()

        refreshElement = page.locator('`nc_1_refresh1`')
        if refreshElement:
            self.logger.error('拖动识别失败，请手动操作')
            
            #   等待人工操作
    
    def handleRequest(self, request: PlayRequest):
        pass


    def handleResponse(self, response: PlayResponse):
        if '?jsv=' not in response.request.url:
            return
        
        method = response.request.method
        self.logger.debug('请求:{url}',url=response.url)
        self.logger.debug('提交数据:{data}',data=response.request.post_data)
        self.urlCreateFunc(response.url, method)

    def handleRequestFinish(self, response: PlayRequest):
        pass
        
    def jsvApiAutoCreate(self, urls:List[str], headless=False):
        '''自动通过URL列表捕获请求并生成API'''

        self.logger.debug('打开链接:{jumpUrl}', jumpUrl=urls)
        playwright = sync_playwright().start()
        iPhone13 = playwright.devices['iPhone 13']
        self.logger.debug('设备列表:{devices}',devices=playwright.devices)
        browser = playwright.chromium.launch(headless=headless, devtools=self.debug)
        context = browser.new_context(
            **iPhone13,
            # is_mobile=False,
            # device_scale_factor=1.0,
        )
        cookie: List[Any] = [{ 'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path} for cookie in self.cookies]
        context.add_cookies(cookie)
        page = context.new_page()
        page.on('request', self.handleRequest)
        page.on('response', self.handleResponse)
        page.on('requestfinished', self.handleRequestFinish)

        for url in urls:
            page.goto(url, wait_until='domcontentloaded')
            page.wait_for_load_state('load')

    def urlCreateFunc(self, api: str, method: str = 'get', func_name: str | None = None, desc: str = ''):
        '''解析API链接为函数'''
        urlObj = urlparse(api)
        
        queryParams = dict(parse_qsl(urlObj.query))
        [platform, service_name, version] = urlObj.path.strip('/').split('/')

        func_name = func_name if func_name else ''.join([i.capitalize() for i in service_name.split('.')])
        if hasattr(self, func_name):
            self.logger.debug('已存在函数:{func_name}',func_name=func_name)
            return
        
        with open(__file__, 'r', encoding='utf-8') as f:
            context = f.read()
            if func_name in context:
                self.logger.debug('已存在函数:{func_name}',func_name=func_name)
                return
        
        for key in queryParams:
            val = queryParams[key]
            if len(re.findall(r'\{.*?\}|\[.*?\]', val)) > 0:
                try:
                    queryParams[key] = json.loads(val)
                except JSONDecodeError as err:
                    queryParams[key] = val
        
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
                fieldStr += f'    {key}: List\n'
            elif type(val) is dict:
                fieldStr += f'    {key}: Dict\n'
            elif type(val) is int:
                fieldStr += f'    {key}: int\n'
            elif type(val) is float:
                fieldStr += f'    {key}: float\n'
            elif type(val) is bool:
                fieldStr += f'    {key}: bool\n'
            else:
                fieldStr += f'    {key}: Any\n'
        
        nowFile = Path(__file__)
        typeFile = nowFile.parent.parent.joinpath('types/taobao.py')
        self.logger.debug(f'写入类型:{typeFile}')
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
    
    def getShop(self, sellerId: str, shopId: str):
        shop = ShopH5(sellerId, shopId)
        shop.cookies = self.cookies
        shop.initShop()

        return shop


class ShopH5(TaobaoH5):

    shopInfo: taobao.ShopInfo
    shopImpression: taobao.ShopImpression

    def __init__(self, sellerId: str, shopId: str) -> None:
        super().__init__()

        self.gongshangUrl = 'https://zhaoshang.tmall.com/maintaininfo/liangzhao.htm?_tb_token_=ea43bb3e1f775&xid=7cbdc4a55de6bd9367aec3bdd88298e7&checkCode=dbpr'
        self.shopInfo = {
            "sellerId": sellerId,
            "shopId": shopId,
            "shopLogo": "",
            "shopName": '',
            "tmall": taobao.BoolStr.false,
        }

        self.shopImpression = {
            'bizLogoPicList': [],
            'aptitude':'',
            'changeSubscribe2Follow': taobao.BoolStr.true,
            'city':'',
            'fansNum':'',
            'goldenSeller': taobao.BoolStr.true,
            'licenseUrl':'',
            'nick':'',
            'ownerChanged': taobao.BoolStr.true,
            'personalManager': taobao.BoolStr.true,
            'sellerId':'',
            'starts':'',
            'tmall': taobao.BoolStr.false,
            'xid':'',
        }

    def initShop(self):
        sellerId = self.shopInfo.get('sellerId')
        shopId = self.shopInfo.get('shopId')

        self.MtopTaobaoShopImpressionIntroGet({'sellerId': sellerId, 'shopId': shopId})
        self.MtopTaobaoShopImpressionLogoGet({'sellerId': sellerId, 'shopId': shopId})

    def tt(self):
        res = self.get('https://zhaoshang.tmall.com/maintaininfo/liangzhao.htm?_tb_token_=ea43bb3e1f775&xid=7cbdc4a55de6bd9367aec3bdd88298e7&checkCode=dbpr', params={

        })
    
    def searchGoods(self, goodsName: str):
        '''搜索商品'''
        pass

    def MtopTaobaoShopImpressionIntroGet(self, data: Any = {}):
        """mtop.taobao.shop.impression.intro.get函数"""

        method = 'get'
        params = {'jsv': '2.6.1', 'appKey': '12574478', 't': '1702987766953', 'sign': '206ee688cc2fea46ff035bccb349579b', 'api': 'mtop.taobao.shop.impression.intro.get', 'v': '1.0', 'type': 'jsonp', 'secType': '1', 'preventFallback': 'true', 'dataType': 'jsonp', 'callback': 'mtopjsonp6', 'data': {'sellerId': '499878111', 'shopId': '62643782'}}
        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.shop.impression.intro.get/1.0/'
        if data:
            params['data'].update(data)

        sellerId = params.get('data',{}).get('sellerId')
        shopId = params.get('data', {}).get('shopId')

        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        if method.upper() == 'GET':
            request_options.setdefault('params', params)
        else:
            request_options.setdefault('data', params)

        request_options.setdefault('headers', {
            **self.headers,
            'Referer': f'https://tbshop.m.taobao.com/app/tb-haodian/h5-pages/impression?sellerId={sellerId}&shopId={shopId}',
        })
        result, res = self._execute(request_options)
        introInfo: taobao.ShopImpression = result.get('data', {}).get('result', {})
        if introInfo:
            self.shopImpression['aptitude'] = introInfo.get('aptitude')
            self.shopImpression['sellerId'] = introInfo.get('sellerId')
            self.shopImpression['tmall'] = introInfo.get('tmall')
            self.shopImpression['starts'] = introInfo.get('starts')
            self.shopImpression['xid'] = introInfo.get('xid')
            self.shopImpression['nick'] = introInfo.get('nick')
            self.shopImpression['city'] = introInfo.get('city')
            self.shopImpression['licenseUrl'] = introInfo.get('licenseUrl')
            self.shopImpression['personalManager'] = introInfo.get('personalManager')
            self.shopImpression['ownerChanged'] = introInfo.get('ownerChanged')

        self.logger.debug(res)
        return result

    def MtopTaobaoShopImpressionLogoGet(self, data: Any = {}):
        """mtop.taobao.shop.impression.logo.get函数"""

        method = 'get'
        params = {'jsv': '2.6.1', 'appKey': '12574478', 't': '1702987766953', 'sign': '206ee688cc2fea46ff035bccb349579b', 'api': 'mtop.taobao.shop.impression.logo.get', 'v': '1.0', 'type': 'jsonp', 'secType': '1', 'preventFallback': 'true', 'dataType': 'jsonp', 'callback': 'mtopjsonp5', 'data': {'sellerId': '499878111', 'shopId': '62643782'}}
        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.shop.impression.logo.get/1.0/'
        if data:
            params['data'].update(data)

        sellerId = params.get('data',{}).get('sellerId')
        shopId = params.get('data', {}).get('shopId')
        request_options = OrderedDict()
        request_options.setdefault('method', method)
        request_options.setdefault('url', url)
        if method.upper() == 'GET':
            request_options.setdefault('params', params)
        else:
            request_options.setdefault('data', params)

        request_options.setdefault('headers', {
            **self.headers,
            'Referer': f'https://tbshop.m.taobao.com/app/tb-haodian/h5-pages/impression?sellerId={sellerId}&shopId={shopId}',
        })
        result, res = self._execute(request_options)
        return result
