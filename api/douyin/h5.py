from ..types import douyin
from ..base import Base, ResponseKw
from PIL import Image
from io import BytesIO, StringIO
from pathlib import Path
from typing import Union, Literal, List, TypedDict, Any, Dict, Tuple
from playwright.sync_api import sync_playwright, Page, Playwright, Browser, BrowserContext
from playwright.sync_api import Response as PlayResponse
from playwright.sync_api import Request as PlayRequest
from urllib.parse import quote_plus, quote, parse_qsl, parse_qs, urlunparse, urlparse
from requests import Response
import time
import base64
import os
import json
import requests
import jsbeautifier

class DouyinH5(Base):

    webmssdk_url:str = 'https://lf-c-flwb.bytetos.com/obj/rc-client-security/c-webmssdk/1.0.0.20/webmssdk.es5.js'
    device_id: str = '7350952832772556339'
    _user_agent: str
    device_info = {
        'width': 1920,
        'height': 1080,
        'cpu_core_num': 16,
        'device_memory': 8,
        'effective_type': '4g',
    }
    playwright: Playwright
    browser: Browser
    context: BrowserContext
    __domain_token: Dict[str,douyin.WareCsrfToken] = {}

    def __init__(self) -> None:
        super().__init__()

        self.verify = False
        self.hooks['response'].append(self.hook_res)

        self.headers.update({
            "accept": "application/json, text/plain, */*",
            # 'Accept':'application/json, text/plain, */*',
            'accept-encoding': 'gzip',
            'user-agent': self.userAgent,
        })
        self.downloadWebmsSdkJs()

        self.init()
    
    def call_request(self, **kwargs):
        self.logger.debug(f'请求参数:{kwargs}')
        url = kwargs.get('url')
        if not url:
            raise Exception('错误')
        
        urlObj = urlparse(url)
        token = self.domain_token(urlObj.hostname)
        if not kwargs.get('headers'):
            kwargs.setdefault('headers',{})
        kwargs['headers'].update({
            'X-Secsdk-Csrf-Token': token
        })


        res = self.request(**kwargs)
        return res

    def hook_res(self, response: Response, *args: Tuple, **kwargs: ResponseKw):
        try:
            res: douyin.ErrorRes = response.json()
            if not res.get('status_code') is None and not res.get('status_msg') is None:
                if res.get('status_code') != 0:
                    self.logger.error(f'请求错误:{res}')
        except json.decoder.JSONDecodeError as err:
            self.logger.debug('无法转为json')
            return
        
    
    def init(self):
        # self.playwright = sync_playwright().start()
        # self.browser = self.playwright.chromium.launch(headless=True, devtools=True)
        # self.context = self.browser.new_context(user_agent=self.userAgent)
        # page = self.context.new_page()
        # page.on('response', self.handleResponse)
        # page.goto('https://www.douyin.com', wait_until='domcontentloaded')
        # self.logger.debug('当前cookie数量:{}', len(self.context.cookies()))
        # time.sleep(10)
        # self.logger.debug('当前cookie数量:{}', len(self.context.cookies()))
        # self.logger.debug('网页内容: {}',page.content())
        # context.evaluate('window.byted_acrawler.frontierSign("aa")')
        # self.get('https://www.douyin.com')
        # self.get('https://sso.douyin.com/get_qrcode/?need_logo=false&need_short_url=false&account_sdk_source=sso&account_sdk_source_info=&biz_trace_id=5a0aa481&aid=6383&language=zh&passport_jssdk_version=3.0.1&device_platform=web_app&msToken=X1mGCvCuuThC08bNQ2qjqpeuAyYcDfTrNTNTcodx5ncfp2MXMYhYfVA_VbxJoI9KTv0LvjiLNZCr3N3VegFzrVcF7U-V4LrKiCQ_39BW7BXayIW2JDkFrq79sIs=',params={
        #     'X-Bogus': self.xBogus
        # })
        # res = self.head('https://www.douyin.com/service/2/abtest_config/',headers={
        #     'Referer':'https://www.douyin.com/user/MS4wLjABAAAA0joAdG_sxN6RJAXJBsXdzh1NzoVNYVgmhGYjooGY9t4',
        #     'X-Secsdk-Csrf-Request': '1',
        #     'X-Secsdk-Csrf-Version':'1.2.22',
        #     **self.headers
        # })
        # if res.status_code != 200:
        #     self.logger.error('获取csrf_session_id的cookie失败')

        # self.post('https://mcs.zijieapi.com/webid', json={
        #     'app_id': 1243,
        #     'referer': 'https://open.douyin.com/platform',
        #     'url': 'https://open.douyin.com/platform/oauth/connect?client_key=awfgitt8rabltohh&response_type=code&scope=user_info&state=6f8521283gAToVCoYXdlbWVfdjKhU6ChTtlZaHR0cHM6Ly9vcGVuLW1pbmlwcm9ncmFtLmJ5dGVkYW5jZS5jb20vYXV0aC9sb2dpbl9zdWNjZXNzLz9zZXJ2aWNlPWh0dHA6Ly9vcGVuLmRvdXlpbi5jb22hVgGhSQChRAChQdEIgKFN0QiAoUivb3Blbi5kb3V5aW4uY29toVIEolBMAKZBQ1RJT06goUzZIGh0dHBzOi8vb3Blbi5kb3V5aW4uY29tL3BsYXRmb3JtoVTZIGIyNjBiMmM5ZjM2ZmMwMTZiMDRkMjZmYTM2MTQ5MTU2oVcAoUYAolNBAKFVw6JNTMI%3D&redirect_uri=https://open.douyin.com/passport/auth/login_success',
        #     'user_agent': self.userAgent,
        #     'user_unique_id': '',
        # })

        # self.post('https://open.douyin.com/aweme/v1/open/auth/info/v4/',data={
        #     'client_key':'',
        #     'scope': 'user_info',
        #     'auth_container': 2,
        #     'source_from': 'WEB',
        #     'without_login': True,
        #     'aid': 1128
        # })

        # #   初始化cookie
        # self.cookies.set('__ac_nonce', self.__ac_nonce, domain='www.douyin.com', path='/')
        # self.cookies.set('__ac_signature', self.__ac_signature, domain='www.douyin.com', path='/')
        # self.cookies.set('ttwid', self.ttwid, domain='www.douyin.com', path='/')
        # self.cookies.set('IsDouyinActive', 'true', domain='.douyin.com', path='/')
        # self.cookies.set('home_can_add_dy_2_desktop', '%221%22', domain='.douyin.com', path='/')
        # self.cookies.set('dy_swidth', str(self.device_info['width']), domain='www.douyin.com', path='/')
        # self.cookies.set('dy_sheight', str(self.device_info['height']), domain='www.douyin.com', path='/')
        # feed_params = json.dumps({
        #     'cookie_enabled': True,
        #     'screen_width': self.device_info['width'],
        #     'screen_height': self.device_info['height'],
        #     'browser_online': True,
        #     'cpu_core_num': self.device_info['cpu_core_num'],
        #     'device_memory': self.device_info['device_memory'],
        #     'downlink': 10,
        #     'effective_type': self.device_info['effective_type'],
        #     'round_trip_time': 50
        # }, separators=(',', ':'))
        # stream_recommend_feed_params = quote(json.dumps(feed_params, separators=(',', ':')))
        # self.cookies.set('stream_recommend_feed_params', stream_recommend_feed_params, domain='.douyin.com', path='/')
        # douyinCookies = self.context.cookies()
        # for cookieItem in douyinCookies:
        #     name = cookieItem.get('name')
        #     value = cookieItem.get('value')
        #     domain = cookieItem.get('domain')
        #     path = cookieItem.get('path')
        #     self.cookies.set(name, value, domain=domain, path=path)
        #     self.logger.debug('设置cookie:{} {} {}', name, value, domain)
        pass
    
    @property
    def userAgent(self):
        if not hasattr(self, '_user_agent'):
            self._user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        return self._user_agent
    
    @property
    def fp(self):
        s_v_web_id = self.cookies.get('s_v_web_id', domain='www.douyin.com', default='')
        if not s_v_web_id is None and len(s_v_web_id) > 0:
            return s_v_web_id
        
        return ''
    
    @property
    def msToken(self):
        token = self.cookies.get('msToken', default='')
        if not token is None and len(token) > 0:
            return token
        
        return self.generate_random_str(124)
    
    def handleResponse(self, response: PlayResponse):
        # self.logger.debug('playwright请求url: {}', response.request.url)
        if 'webmssdk.es5.js' not in response.request.url:
            return
        self.logger.debug('加载js')
    
    def domain_token(self, url: str):
        urlObj = urlparse(url)
        if not urlObj.hostname:
            raise Exception('无法解析的url:{}'.format(url))
        
        tokenMap = self.__domain_token.get(urlObj.hostname)
        if tokenMap and tokenMap['expiredAt'] > (time.time() * 1000):
            return tokenMap['value']
        else:
            tokenMap = self.getCsrfToken(urlObj.hostname, urlObj.path)
            self.__domain_token[urlObj.hostname] = tokenMap
        
        return self.__domain_token[urlObj.hostname]['value']
    
    def X_Bogus(self, params: dict):
        # if isinstance(params, dict):
        #     strParams = map(lambda item:item if isinstance(item[1], str) else str(item[1]), params.items())
        #     params = '&'.join(map(lambda item:'='.join(item),strParams))
        # xBogus = self.context.pages[0].evaluate('(params)=>window.byted_acrawler.frontierSign(params)', params)
        # if not isinstance(xBogus, dict):
        #     self.logger.error('获取X-Bogus失败:', xBogus)
        #     return xBogus
        # out = self.runCmd(f'node webmssdk.es5.js "{params}"')
        # if out:
        #     data = json.loads(out.replace("'",'"'))
        #     return data['X-Bogus']
        return ''
    
    def defaultParams(self, insert_index: Union[int,None] = None, **kwargs):
        '''参数很重要，缺少则不会返回数据，并且顺序也重要'''
        params_list = [
            ('device_platform', 'webapp'), 
            ('aid', '6383'), 
            ('channel', 'channel_pc_web'), 
            ('publish_video_strategy_type', '2'), 
            ('source', 'channel_pc_web'), 
            ('personal_center_strategy', '1'), 
            ('pc_client_type', '1'), 
            ('version_code', '170400'), 
            ('version_name', '17.4.0'), 
            ('cookie_enabled', 'true'), 
            ('screen_width', str(self.device_info['width'])), 
            ('screen_height', str(self.device_info['height'])), 
            ('browser_language', 'zh-CN'), 
            ('browser_platform', 'Win32'), 
            ('browser_name', 'Chrome'), 
            ('browser_version', '123.0.0.0'), 
            ('browser_online', 'true'), 
            ('engine_name', 'Blink'), 
            ('engine_version', '123.0.0.0'), 
            ('os_name', 'Windows'), 
            ('os_version', '10'), 
            ('cpu_core_num', str(self.device_info['cpu_core_num'])), 
            ('device_memory', str(self.device_info['device_memory'])), 
            ('platform', 'PC'), 
            ('downlink', '10'), 
            ('effective_type', '4g'), 
            ('round_trip_time', '50'), 
            ('webid', '7350983312603153958')
        ]

        if not insert_index is None:
            if insert_index <= 0:
                raise Exception('参数的顺序不能小于0')
            kwargs_list = list(kwargs.items())
            kwargs_list.reverse()
            for kwargs_item in kwargs_list:
                params_list.insert(insert_index - 1, kwargs_item)

        return dict(params_list)

    @property
    def douyinDefaultHeader(self):
        pass

    @property
    def douyinSecsdkHeader(self):
        return {
            'X-Secsdk-Csrf-Request': '1',
            'X-Secsdk-Csrf-Version':'1.2.22',
        }

    def downloadWebmsSdkJs(self,refresh: bool = False):
        webssdkPath = self.work_dir.joinpath('webmssdk.es5.js')
            
        if webssdkPath.exists():
            if refresh:
                webssdkPath.unlink()
            else:
                return
        
        res = self.get(self.webmssdk_url)
        res.encoding = 'utf-8'
        if res.status_code != 200:
            self.logger.error(res.text)
            return
        
        js = f'''
window = global;
window['__ac_referer'] = "{self.userAgent}"
document = {{}};
document.addEventListener = function () {{}};
navigator = {{
    userAgent:"{self.userAgent}",
}};
''' 
        options = jsbeautifier.default_options()
        options.indent_size = 4
        options.indent_char = ' '
        options.preserve_newlines = True
        newJs = jsbeautifier.beautify(res.text, options)

        with open(webssdkPath, 'w', encoding='utf-8') as f:
            f.write(js)
            f.write(newJs)
            f.write('''

if(process.argv.length > 2){
    console.log(window.byted_acrawler.frontierSign(process.argv[2]));
}
''')

    def checkQr(self, token: str) -> Union[str, None]:
        res = self.get('https://sso.douyin.com/check_qrconnect/', params={
            "service":"https://www.douyin.com",
            "token": token,
            "need_logo":"false",
            "is_frontier":"false",
            "need_short_url":"false",
            "device_platform":"web_app",
            "aid":"6383",
            "account_sdk_source":"sso",
            "sdk_version":"2.2.7-beta.6",
            "language":"zh",
            "verifyFp": self.fp,
            "fp": self.fp,
            "msToken": self.msToken,
            "X-Bogus":"DFSzswVuzeD3FX/Itubv5l9WX7rO"
        })
        result: douyin.QrCheckRes = res.json()
        self.logger.debug('检查数据:{result}', result=result)
        scanStatus = result.get('data').get('status')
        if scanStatus in [douyin.QrStatus.已扫码, douyin.QrStatus.已扫码2]:
            self.logger.debug('已扫码')
        elif scanStatus in [douyin.QrStatus.未扫码, douyin.QrStatus.未扫码2]:
            self.logger.debug('未扫码')
        elif scanStatus in [douyin.QrStatus.扫码成功]:
            return result.get('data').get('redirect_url')

        #   得到ticket
        # 请求https://www.douyin.com/login/?next=https%3A%2F%2Fwww.douyin.com&ticket=337c287605d767929b8e66e579a14ace_lq
        # 重定向 https://www.douyin.com/passport/sso/login/callback/?ticket=337c287605d767929b8e66e579a14ace_lq&next=https%3A%2F%2Fww
        return

    def qrLogin(self, timeout: int = 60):
        res = self.get('https://sso.douyin.com/get_qrcode/', params={
            'service': 'https://www.douyin.com',
            'need_logo': False,
            'is_frontier': False,
            'need_short_url': False,
            'device_platform': 'web_app',
            'aid': 6383,
            'account_sdk_source': 'sso',
            'sdk_version': '2.2.7-beta.6',
            'language': 'zh',
            'verifyFp': self.fp,
            'fp': self.fp,
            'msToken': self.msToken,
            'X-Bogus': 'DFSzswVuzeD3FX/Itubv5l9WX7rO',
        })
        result: douyin.QrLoginRes = res.json()
        if result.get('error_code') != 0:
            self.logger.error('请求失败:{result}', result=result)
            return
        
        qrcode = result.get('data').get('qrcode')
        base64Img = base64.b64decode(qrcode)
        img = Image.open(BytesIO(base64Img))
        img.save('qrcode.png')
        os.system('start qrcode.png')

        token = result.get('data').get('token')

        while timeout > 0:
            jumpUrl = self.checkQr(token)
            if jumpUrl:
                self.get(jumpUrl)
                return True
            time.sleep(1)
            timeout -= 1

        return False
    
    def qrLogin2(self):
        
        res = self.get('https://sso.douyin.com/check_qrconnect/', params={
            'service': '',
            'token':'',
            'need_logo': False,
            'is_frontier': False,
            'need_short_url': False,
            'device_platform': 'web_app',
            'aid': 6383,
            'account_sdk_source': 'sso',
            'sdk_version': '2.2.7-beta.6',
            'language': 'zh',
            'verifyFp': '',
            'fp': '',
            'msToken':'',
            'X-Bogus': '',
        })
    
    @property
    def ttwid(self):
        if not self.cookies.get('ttwid'):
            res = self.post('https://ttwid.bytedance.com/ttwid/union/register/', json={
                "region":"cn",
                "aid":1768,
                "needFid": False,
                "service":"www.ixigua.com",
                "migrate_info":{
                    "ticket":"",
                    "source":"node"
                },
                "cbUrlProtocol":"https",
                "union": True
            })
            # res = self.get('https://www.douyin.com/user/MS4wLjABAAAA0joAdG_sxN6RJAXJBsXdzh1NzoVNYVgmhGYjooGY9t4',headers={
            #     'Referer': 'https://www.douyin.com/user/MS4wLjABAAAA0joAdG_sxN6RJAXJBsXdzh1NzoVNYVgmhGYjooGY9t4',
            # })
            # res = self.get('https://www.douyin.com/discover?modal_id=7352081640375553299')
            self.logger.debug(res.request.headers)

        ttwidStr = self.cookies.get('ttwid')
        if ttwidStr:
            return ttwidStr

        self.logger.error('获取ttwid失败')
        return ''

    def otherProfile(self, sec_user_id: str):
        '''用户信息'''
        params = {
            **self.defaultParams(6, sec_user_id=sec_user_id),
        }

        url = 'https://www.douyin.com/aweme/v1/web/user/profile/other/'
        res = self.get(url, params=params, headers={
            'referer': f'https://www.douyin.com/user/{sec_user_id}',
            'User-Agent': self.userAgent,
            # 'cookie':'ttwid=1%7CL2R4AcseQJgu0aUZateAwjHw13oU64Z6V77CdDL2X-Q%7C1711534190%7C4dd04c1852a3d72b8384444530be7aa41200c31696e751a49ba671380227b856'
        })

        data: douyin.ProfileOtherResType = res.json()
        
        return data['user']
    
    def videoList(self, sec_user_id: str):
        '''作品列表
        API: max_cursor=0&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18'''
        url = 'https://www.douyin.com/aweme/v1/web/aweme/post/'
        params = {
            **self.defaultParams(
                4,
                sec_user_id=sec_user_id,
                max_cursor='0',
                locate_query='false',
                show_live_replay_strategy='1',
                need_time_list=1,
                time_list_query=0,
                whale_cut_token='',
                cut_version=1,
                count=18
            ),
            'msToken': '',
        }
        res = self.get(url, params=params, headers={
            'Referer': f'https://www.douyin.com/user/{sec_user_id}'
        })

        print(res.text)
    
    def videoMixList(self, sec_user_id: str):
        '''用户作品合集列表'''

        url = 'https://www.douyin.com/aweme/v1/web/mix/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAqUUm4EffFejs18KzTEf6qx-f4mYGLazKKgdGPVfzGO9fAAoNeTi9xrJw8VnLsvKx&req_from=channel_pc_web&cursor=0&count=12&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7353624324970219043'
    
    def videlLocateList(self, sec_user_id: str, max_cursor: int = 0):
        url = 'https://www.douyin.com/aweme/v1/web/locate/post/'
        'locate_item_id=7338022829318819107&locate_item_cursor=1708516602000&locate_query=true'
        params = {
            'sec_user_id': sec_user_id,
            'max_cursor': max_cursor,
            'locate_item_id':'7338022829318819107',
        }
        res = self.get(url)
    
    def videoComments(self, aweme_id: str, cursor=1,count = 20):
        url = 'https://www.douyin.com/aweme/v1/web/comment/list/'
        params = {
            **self.defaultParams(4),
            "aweme_id":aweme_id,
            'cursor': cursor,
            'count': count
        }

        res = self.get(url,params=params, headers={
            'referer':'https://www.douyin.com/discover?modal_id=7353827429447699712',
            'host': 'www.douyin.com',
            'cookie':'ttwid=1%7CP_yaaU2EJwDb6axCx1ejJEO8Udl76Qtud0WYR0yFNpA%7C1712149098%7C72cb56a9931184024ec6f3a5e2b4efdc52c53e901bae32f6a65ac6ac48060bd8; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=eea59a7c4564724e9b4dc25572a9f83a; passport_csrf_token_default=eea59a7c4564724e9b4dc25572a9f83a; bd_ticket_guard_client_web_domain=2; download_guide=%223%2F20240403%2F0%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; csrf_session_id=3bef5b4a9ff04d33c1c3eb6e23298a57; xgplayer_user_id=902129266265; xg_device_score=7.90435294117647; __live_version__=%221.1.1.9068%22; live_can_add_dy_2_desktop=%220%22; live_use_vvc=%22false%22; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_signature=_02B4Z6wo00f01.bzkjAAAIDAy1qIr.46DCv205aAAJu8c4; strategyABtestKey=%221712208759.823%22; GlobalGuideTimes=%221712208983%7C0%22; xgplayer_device_id=26858847177; s_v_web_id=verify_lul0plcd_f8463012_e580_5a22_ac47_0ac6c2a4c063; n_mh=6qq-cGgTT9fkYiwsN45Jh1uyewEXJiS4wSqKokLJKfI; _bd_ticket_crypt_doamin=2; LOGIN_STATUS=1; __security_server_data_status=1; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; d_ticket=031e11614692a594af527a4f35527105d6a25; passport_assist_user=CjxmqckqHS9cNNXQKiDoomR2Ip6CPjc06gE08Ogw7u31i2XbZRcjgVsD6suNoVvsO9hruMrYsOlsGB9vtfQaSgo8Z__4BxWBkFivXNBezpLEHrFJAf_8qdROk95rQIK9t5OWWKH2RZHGzFvNL76qaE-lbqXflvrrjGjcr93XEP3izQ0Yia_WVCABIgED-2MemQ%3D%3D; sso_uid_tt=29db5759c7a863686fbc6282bf936250; sso_uid_tt_ss=29db5759c7a863686fbc6282bf936250; toutiao_sso_user=df5d7c87c54beb0d0b6b17c5402a64e5; toutiao_sso_user_ss=df5d7c87c54beb0d0b6b17c5402a64e5; sid_ucp_sso_v1=1.0.0-KDY3Y2ZhYTY5NWMyMjhkNjhlMzQxNDU0MGY5ODE5MmMxZjI0OTg3NGMKHQiSvPzv9AEQ5Lu6sAYY7zEgDDCiv6_MBTgGQPQHGgJscSIgZGY1ZDdjODdjNTRiZWIwZDBiNmIxN2M1NDAyYTY0ZTU; ssid_ucp_sso_v1=1.0.0-KDY3Y2ZhYTY5NWMyMjhkNjhlMzQxNDU0MGY5ODE5MmMxZjI0OTg3NGMKHQiSvPzv9AEQ5Lu6sAYY7zEgDDCiv6_MBTgGQPQHGgJscSIgZGY1ZDdjODdjNTRiZWIwZDBiNmIxN2M1NDAyYTY0ZTU; passport_auth_status=6e6355a233edc2a2f441c60ba6b178d6%2C29b855bbc880652916e91bc5eec68336; passport_auth_status_ss=6e6355a233edc2a2f441c60ba6b178d6%2C29b855bbc880652916e91bc5eec68336; uid_tt=4c425b9b724457ce67f40c66d2f25491; uid_tt_ss=4c425b9b724457ce67f40c66d2f25491; sid_tt=8ce8edd349ea9e523a1ab56826a156f2; sessionid=8ce8edd349ea9e523a1ab56826a156f2; sessionid_ss=8ce8edd349ea9e523a1ab56826a156f2; store-region=cn-hb; store-region-src=uid; _bd_ticket_crypt_cookie=d44b93ba1fa2a1eaa729954eb164e71d; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQTlaQ1dLTFh6NnFtT1pua1BiYTFaa3daQjY5N2pMdE1MZzVkZVVxUWl1SzJ1OVZ2eVM5SkhWUEUyWWVWUVVhNmExMHB3SGxPWHppNXYwMEtsbUZpalU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; sid_guard=8ce8edd349ea9e523a1ab56826a156f2%7C1712233961%7C5183998%7CMon%2C+03-Jun-2024+12%3A32%3A39+GMT; sid_ucp_v1=1.0.0-KDYzNmY2MWIwZDY4NzFjYTAzNDZmNjQ2ZjUyNzUxYTY0OWE0MGRhZDAKGQiSvPzv9AEQ6bu6sAYY7zEgDDgGQPQHSAQaAmxxIiA4Y2U4ZWRkMzQ5ZWE5ZTUyM2ExYWI1NjgyNmExNTZmMg; ssid_ucp_v1=1.0.0-KDYzNmY2MWIwZDY4NzFjYTAzNDZmNjQ2ZjUyNzUxYTY0OWE0MGRhZDAKGQiSvPzv9AEQ6bu6sAYY7zEgDDgGQPQHSAQaAmxxIiA4Y2U4ZWRkMzQ5ZWE5ZTUyM2ExYWI1NjgyNmExNTZmMg; home_can_add_dy_2_desktop=%221%22; publish_badge_show_info=%220%2C0%2C0%2C1712233965432%22; odin_tt=cc48278aebcee3cb75cf143e567c55b253d0cd29ad06bf6c1dcef68adeb5debd04b40d22a0b822f3373fb115a467adf1; msToken=RtGlT1FVMcYm8sdZDpxtEk1A7ehXyXtAGfhKbnldEkWmS6Aj4yXPDrQjMTZlMlpVi-6KmYV0YHi-m3K3GCfhyQ5fldkgHZRxNQcZkd1ARbT-Wq0k_I_DiPAD-29o6Q==; IsDouyinActive=true',
            'user-agent':self.userAgent,
        })
        # print(res.request.headers)
        #   错误返回
        #   {"status_code":5,"status_msg":"","log_pb":{"impr_id":"202404042053520DD3E00E46C79CCA6D42"}}
        resp: douyin.VideoCommentType = res.json()
        self.renderType('VideoCommentDetail', resp['comments'][0])
    
    def queryUserInfo(self, sec_user_id: str):
        url = 'https://www.douyin.com/aweme/v1/web/im/user/info/'
        params = {
            **self.defaultParams(1),
        }

        res = self.post(url, params=params, data={'sec_user_ids': [sec_user_id]},headers={
            'referer':f'https://www.douyin.com/user/{sec_user_id}',
            'X-Secsdk-Csrf-Token': self.domain_token(url)
        })
        resp = res.json()

    def hotSearchList(self):
        url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&main_billboard_count=5&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7353624324970219043'
    
    def search(self,keyword: str, offset: int = 0, count: int = 12):
        url = 'https://www.douyin.com/aweme/v1/web/discover/search/'
        params = {
            'search_channel':'aweme_user_web',
            'keyword': keyword,
            'search_source': 'normal_search',
            'query_correct_type': '1',
            'is_filter_search': '0',
            'offset': offset,
            'count': count,
            'need_filter_settings': 1,
        }

        res = self.get(url, params=params)

        resp = res.json()


    def report(self):
        res = self.post('https://mssdk.bytedance.com/web/report',params={
            'msToken': self.msToken,
            'X-Bogus': '',
        }, headers={'cookie': f'msToken={self.msToken}'})
        # print(res)
    
    def check(self):
        res = self.get('https://tnc3-bjlgy.zijieapi.com/get_domains/v5/',params={
            'tnc_js_sdk_version': '2.1.0.0',
            'device_platform': 'pc',
            'aid': '6383',
            'device_id': self.device_id,
            'web_service': ''
        })
        print(res.json())
    
    def renderType(self,name:str, params: Any):
        if not isinstance(params, dict):
            return
        
        params_type_template = '''
class {name}Type(TypedDict):
{paramsStr}
'''

        paramsStr = ''
        for key in params:
            paramsStr += f'    {key}: {self.typeStr(params[key])}\n'
        
        douyinTypePath = Path(__file__).parent.parent.joinpath('types/douyin.py')
        with open(douyinTypePath, 'a+', encoding='utf-8') as f:
            f.write(params_type_template.format(name=name,paramsStr=paramsStr))
    
    def getDeviceInfoParams(self):
        common_search_params = {"device_platform":"webapp","aid":6383,"channel":"channel_pc_web"}
        return {"version_code":"290100","version_name":"29.1.0","os":"web","device_brand":"web","device_model":"web","device_type":"web_device"}
    
    def getNavigatorParams(self):
        return {"cookie_enabled":True,"screen_width":1920,"screen_height":1080,"browser_language":"zh-CN","browser_platform":"Win32","browser_name":"Chrome","browser_version":"123.0.0.0","browser_online":True,"engine_name":"Blink","engine_version":"123.0.0.0","os_name":"Windows","os_version":"10","cpu_core_num":16,"device_memory":8,"platform":"PC","downlink":10,"effective_type":"4g","round_trip_time":50}
    
    def getCsrfToken(self, domain: str, path: str) -> douyin.WareCsrfToken:
        '''获取csrftoken'''
        if not domain.startswith('https://'):
            domain = f'https://{domain}'

        res = self.head(f'{domain}{path}',headers={
            # 'x-secsdk-csrf-request': '1',
            # 'x-secsdk-csrf-version': '1.2.22',
            **self.douyinSecsdkHeader
        })
        if res.status_code != 200:
            raise Exception('获取token失败')
        
        headerVal = res.headers.get('x-ware-csrf-token')
        if not headerVal:
            raise Exception('获取csrf token失败')
        
        tokenValid,token,maxAge,*other = headerVal.split(',')
        if tokenValid != '0':
            raise Exception(f'错误的数值:{headerVal}')
        
        return {
            'value': token,
            'expiredAt': int(time.time() * 1000) + int(maxAge),
            'timeout': False
        }
        

        


'''
这3个cookie才能请求到数据
sid_tt=876ef0e20d
sessionid=876ef0
sessionid_ss=876e

{"s0":"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=","s1":"Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=","s2":"Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=","s3":"ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe","s4":"Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"}
'''