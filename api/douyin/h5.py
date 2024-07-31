from ..types import douyin
from ..base import Base, ResponseKw
from PIL import Image
from io import BytesIO, StringIO
from pathlib import Path
from typing import Union, Literal, List, TypedDict, Any, Dict, Tuple
from playwright.sync_api import (
    sync_playwright,
    Page,
    Playwright,
    Browser,
    BrowserContext,
)
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
import datetime
import re
import string
import random
import execjs


class DouyinH5(Base):

    bdms_url: str = (
        "https://lf-headquarters-speed.yhgfb-cn-static.com/obj/rc-client-security/web/stable/1.0.1.5/bdms.js"
    )
    _user_agent: str
    device_info = {
        "width": 1920,
        "height": 1080,
        "cpu_core_num": 16,
        "device_memory": 8,
        "effective_type": "4g",
    }
    playwright: Playwright
    browser: Browser
    context: BrowserContext
    __domain_token: Dict[str, douyin.WareCsrfToken] = {}
    _webid: str = ""

    def __init__(self) -> None:
        super().__init__()

        self.verify = False
        self.hooks["response"].append(self.hook_res)

        self.headers.update(
            {
                "accept": "application/json, text/plain, */*",
                # 'Accept':'application/json, text/plain, */*',
                "accept-encoding": "gzip",
                "user-agent": self.userAgent,
            }
        )
        self.downloadBdmsJs()

        self.init()

    def call_request(self, **kwargs):
        self.logger.debug(f"请求参数:{kwargs}")
        url = kwargs.get("url")
        if not url:
            raise Exception("错误")

        urlObj = urlparse(url)
        token = self.domain_token(urlObj.hostname)
        if not kwargs.get("headers"):
            kwargs.setdefault("headers", {})
        kwargs["headers"].update({"X-Secsdk-Csrf-Token": token})

        res = self.request(**kwargs)
        return res

    def hook_res(self, response: Response, *args: Tuple, **kwargs: ResponseKw):
        setCookie = response.headers.get("set-cookie")
        if setCookie:
            self.logger.debug(f"设置cookie:{response.url}")
            self.logger.debug(f"cookie:{setCookie}")
        msToken = response.headers.get('X-Ms-Token')
        if msToken:
            self.logger.debug(f'返回token:{msToken}')
        contentType = response.headers.get("content-type")
        if not contentType:
            return

        if "json" in contentType:
            try:
                res: douyin.ErrorRes = response.json()
                if (
                    not res.get("status_code") is None
                    and not res.get("status_msg") is None
                ):
                    if res.get("status_code") != 0:
                        self.logger.error(f"请求错误:{res}")
            except json.decoder.JSONDecodeError as err:
                self.logger.debug("无法转为json")
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

        res = self.head(
            "https://www.douyin.com/service/2/abtest_config/",
            headers={
                "Referer": "https://www.douyin.com/help",
                "X-Secsdk-Csrf-Request": "1",
                "X-Secsdk-Csrf-Version": "1.2.22",
                "User-Agent": self.userAgent,
            },
        )
        # if res.status_code != 200:
        #     self.logger.error('获取csrf_session_id的cookie失败')

        res = self.post(
            "https://mcs.zijieapi.com/webid",
            json={
                "app_id": 2018,
                "referer": "",
                "url": "https://www.douyin.com/help",
                "user_agent": self.userAgent,
                "user_unique_id": "",
            },
            headers={
                "Origin": "",
                "Referer": "",
            },
        )
        if res.status_code == 200:
            resj = res.json()
            if resj.get('web_id'):
                self._webid = resj.get('web_id')

        # self.post('https://open.douyin.com/aweme/v1/open/auth/info/v4/',data={
        #     'client_key':'',
        #     'scope': 'user_info',
        #     'auth_container': 2,
        #     'source_from': 'WEB',
        #     'without_login': True,
        #     'aid': 1128
        # })

        # #   初始化cookie
        self.cookies.set(
            "s_v_web_id", self.verifyFp(), domain="www.douyin.com", path="/"
        )
        # self.cookies.set('__ac_nonce', '0661a40ef0097fc671295', domain='.douyin.com', path='/')
        # self.cookies.set('__ac_signature', '_02B4Z6wo00f01odwKXQAAIDButkz6ZY-4J6HUC3AAMfS28', domain='.douyin.com', path='/')
        # self.cookies.set('ttwid', self.ttwid, domain='www.douyin.com', path='/')
        # self.cookies.set('IsDouyinActive', 'true', domain='.douyin.com', path='/')
        self.cookies.set(
            "home_can_add_dy_2_desktop", "%221%22", domain=".douyin.com", path="/"
        )
        self.cookies.set(
            "download_guide", "%221%2F20240728%2F0%22", domain=".douyin.com", path="/"
        )
        self.cookies.set("IsDouyinActive", "true", domain=".douyin.com", path="/")
        self.cookies.set(
            "FORCE_LOGIN",
            "%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D",
            domain=".douyin.com",
            path="/",
        )
        self.cookies.set(
            "dy_swidth",
            str(self.device_info["width"]),
            domain="www.douyin.com",
            path="/",
        )
        self.cookies.set(
            "dy_sheight",
            str(self.device_info["height"]),
            domain="www.douyin.com",
            path="/",
        )
        feed_params = json.dumps(
            {
                "cookie_enabled": True,
                "screen_width": self.device_info["width"],
                "screen_height": self.device_info["height"],
                "browser_online": True,
                "cpu_core_num": self.device_info["cpu_core_num"],
                "device_memory": self.device_info["device_memory"],
                "downlink": 10,
                "effective_type": self.device_info["effective_type"],
                "round_trip_time": 50,
            },
            separators=(",", ":"),
        )
        stream_recommend_feed_params = quote(
            json.dumps(feed_params, separators=(",", ":"))
        )
        self.cookies.set(
            "stream_recommend_feed_params",
            stream_recommend_feed_params,
            domain=".douyin.com",
            path="/",
        )
        self.cookies.set(
            "device_web_cpu_core",
            str(self.device_info["cpu_core_num"]),
            domain=".douyin.com",
            path="/user",
        )
        self.cookies.set(
            "device_web_memory_size",
            str(self.device_info["device_memory"]),
            domain=".douyin.com",
            path="/user",
        )
        # douyinCookies = self.context.cookies()
        # for cookieItem in douyinCookies:
        #     name = cookieItem.get('name')
        #     value = cookieItem.get('value')
        #     domain = cookieItem.get('domain')
        #     path = cookieItem.get('path')
        #     self.cookies.set(name, value, domain=domain, path=path)
        #     self.logger.debug('设置cookie:{} {} {}', name, value, domain)
        pattern = r'\\"user_unique_id\\":\\"(\d+)\\"'
        res = self.get(
            "https://www.douyin.com/help",
            headers={
                "Referer": "https://www.douyin.com/help",
                "User-Agent": self.userAgent,
                "Sec-Fetch-Dest": "document",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
            },
        )
        res = self.get(
            "https://www.douyin.com/", headers={"sec-fetch-dest": "document"}
        )
        matchWebid = re.search(pattern, res.text)
        if matchWebid:
            self._webid = matchWebid.group(1)
        self.DOUYIN_SIGN = execjs.compile(
            open(
                self.work_dir.joinpath("api", "douyin", "douyin.js"), encoding="utf8"
            ).read()
        )

        # #   获取msToken
        # params = {
        #     'dataType': 8,
        #     'magic': 538969122,
        #     # 'strData': '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',
        #     'tspFormClient': 1722263741394,
        #     'ulr': 0,
        #     'version': 1
        # }

        # params.update({
        #     'strData': self.replay(params)
        # })
        # res = self.post('https://mssdk.bytedance.com/web/common',params)
        pass

    def strData(self,x, y):
        b = [i for i in range(256)]
        c = 0
        d = ""
        for i in range(256):
            c = (c + b[i] + ord(x[i % len(x)])) % 256
            a = b[i]
            b[i] = b[c]
            b[c] = a
        e = 0
        c = 0
        for i in range(len(y)):
            e = (e + 1) % 256
            c = (c + b[e]) % 256
            a = b[e]
            b[e] = b[c]
            b[c] = a
            d += chr(ord(y[i]) ^ b[(b[e] + b[c]) % 256])
        return d

    @property
    def userAgent(self):
        if not hasattr(self, "_user_agent"):
            self._user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        return self._user_agent

    @property
    def fp(self):
        """verify_fp的数据"""
        s_v_web_id = self.cookies.get("s_v_web_id", domain="www.douyin.com", default="")
        if not s_v_web_id is None and len(s_v_web_id) > 0:
            return s_v_web_id

        return ""

    @property
    def msToken(self):
        token = self.cookies.get("msToken", default="")
        if not token is None and len(token) > 0:
            return token

        return self.generate_random_str(124)

    @property
    def passportCsrfToken(self):
        return self.cookies.get("passport_csrf_token", default="")

    @property
    def webid(self):
        '''游客id'''
        return self._webid

    @property
    def hasLogin(self):
        login_cookies = ["sid_tt", "sessionid", "sessionid_ss", "sid_guard"]
        if not any(map(lambda cookieName: self.cookies.get(cookieName), login_cookies)):
            return False

        return True

    def verifyFp(self, mseconds: str | int = ""):

        signString = string.digits + string.ascii_uppercase + string.ascii_lowercase
        signLen = len(signString)
        mseconds = mseconds if mseconds else int(time.time() * 1000)
        nowSeonds = self.toString(int(f"{mseconds}"), 36)
        signList = [""] * 36
        signList[8] = "_"
        signList[13] = "_"
        signList[18] = "_"
        signList[23] = "_"
        signList[14] = "4"

        for o in range(36):
            if not signList[o]:
                i = 0 | (int(random.random() * signLen))
                if o == 19:
                    signList[o] = signString[3 & i]
                else:
                    signList[o] = signString[i]

        return f"verify_{nowSeonds}_{''.join(signList)}"

    def setSessionid(self, sessionid: str):
        login_cookies = ["sid_tt", "sessionid", "sessionid_ss"]
        sid_guard = login_cookies.pop()
        for cookieName in login_cookies:
            self.cookies.set(cookieName, sessionid, domain=".douyin.com", path="/")

    def handleResponse(self, response: PlayResponse):
        # self.logger.debug('playwright请求url: {}', response.request.url)
        if "webmssdk.es5.js" not in response.request.url:
            return
        self.logger.debug("加载js")

    def domain_token(self, url: str):
        urlObj = urlparse(url)
        if not urlObj.hostname:
            raise Exception("无法解析的url:{}".format(url))

        tokenMap = self.__domain_token.get(urlObj.hostname)
        if tokenMap and tokenMap["expiredAt"] > (time.time() * 1000):
            return tokenMap["value"]
        else:
            tokenMap = self.getCsrfToken(urlObj.hostname, urlObj.path)
            self.__domain_token[urlObj.hostname] = tokenMap

        return self.__domain_token[urlObj.hostname]["value"]

    def X_Bogus(self, params: dict):
        if isinstance(params, dict):
            strParams = map(
                lambda item: item if isinstance(item[1], str) else str(item[1]),
                params.items(),
            )
            # params = "&".join(map(lambda item: "=".join(item), strParams))
        # xBogus = self.context.pages[0].evaluate('(params)=>window.byted_acrawler.frontierSign(params)', params)
        # if not isinstance(xBogus, dict):
        #     self.logger.error('获取X-Bogus失败:', xBogus)
        #     return xBogus
        # out = self.runCmd(f'node webmssdk.es5.js "{params}"')
        # if out:
        #     data = json.loads(out.replace("'",'"'))
        #     return data['X-Bogus']

        return ""

    def a_bogus(self, params: dict | str):
        if isinstance(params, dict):
            strParams = map(
                lambda item: item if isinstance(item[1], str) else str(item[1]),
                params.items(),
            )
            params = "&".join(map(lambda item: "=".join(item), strParams))
        call_name = "sign_datail"
        # if 'reply' in uri:
        #     call_name = 'sign_reply'
        out = self.DOUYIN_SIGN.call(call_name, params, self.userAgent)
        # out = self.runCmd(f'node bdms.js "{params}"')
        return out
    
    def replay(self, params: dict | str):
        if isinstance(params, dict):
            strParams = map(
                lambda item: item if isinstance(item[1], str) else str(item[1]),
                params.items(),
            )
            params = "&".join(map(lambda item: "=".join(item), strParams))
        call_name = "sign_reply"
        # if 'reply' in uri:
        #     call_name = 'sign_reply'
        out = self.DOUYIN_SIGN.call(call_name, params, self.userAgent)
        # out = self.runCmd(f'node bdms.js "{params}"')
        return out

    def defaultParams(self, insert_index: Union[int, None] = None, **kwargs):
        """参数很重要，缺少则不会返回数据，并且顺序也重要"""
        params_list = [
            ("device_platform", "webapp"),
            ("aid", "6383"),
            ("channel", "channel_pc_web"),
            ("publish_video_strategy_type", "2"),
            ("source", "channel_pc_web"),
            ("personal_center_strategy", "1"),
            ("pc_client_type", "1"),
            ("version_code", "170400"),
            ("version_name", "17.4.0"),
            ("cookie_enabled", "true"),
            # ('screen_width', str(self.device_info['width'])),
            # ('screen_height', str(self.device_info['height'])),
            ("browser_language", "zh-CN"),
            ("browser_platform", "Win32"),
            ("browser_name", "Chrome"),
            ("browser_version", "123.0.0.0"),
            ("browser_online", "true"),
            ("engine_name", "Blink"),
            ("engine_version", "123.0.0.0"),
            ("os_name", "Windows"),
            ("os_version", "10"),
            ("cpu_core_num", str(self.device_info["cpu_core_num"])),
            ("device_memory", str(self.device_info["device_memory"])),
            ("platform", "PC"),
            ("downlink", "10"),
            ("effective_type", "4g"),
            ("round_trip_time", "50"),
            ("webid", self.webid),
        ]

        if not insert_index is None:
            if insert_index <= 0:
                raise Exception("参数的顺序不能小于0")
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
            "X-Secsdk-Csrf-Request": "1",
            "X-Secsdk-Csrf-Version": "1.2.22",
        }

    def downloadBdmsJs(self, refresh: bool = False):
        webssdkPath = self.work_dir.joinpath("bdms.js")

        if webssdkPath.exists():
            if refresh:
                webssdkPath.unlink()
            else:
                return

        res = self.get(self.bdms_url)
        res.encoding = "utf-8"
        if res.status_code != 200:
            self.logger.error(res.text)
            return

        js = f"""
window = globalThis || {{}};
window.requestAnimationFrame = function(){{}};
window.XMLHttpRequest = function(){{}};
window.navigator = {{
    userAgent: "{self.userAgent}"
}}
window.innerWidth = 1920;
window.innerHeight = 215;
window.outerWidth = 1392;
window.outerHeight = 1920;
window.screenX = 1920;
window.screenY = 0;
window.pageYOffset = 5300;

window.screen = {{
    availHeight:1392,
    availLeft: 1920,
    availTop: 0,
    availWidth: 1920,
    colorDepth: 24,
    height: {self.device_info['height']},
    isExtended: true,
    onchange: null,
    pixelDepth: 24,
    width: {self.device_info['width']}
}}

window.document = {{}};
"""
        options = jsbeautifier.default_options()
        options.indent_size = 4
        options.indent_char = " "
        options.preserve_newlines = True
        newJs = jsbeautifier.beautify(res.text, options)

        with open(webssdkPath, "w", encoding="utf-8") as f:
            f.write(js)
            f.write(newJs)
            f.write(
                f"""

if(process.argv.length > 2){{
    console.log(bdms.init._v[2].p[42]._u.apply(null, [1582, [0, 1, 8, process.argv[2], "", "{self.userAgent}"], 6, bdms.init._v[2].p[42]._v[2], null]));
}}
"""
            )

    def checkQr(self, token: str) -> Union[str, None]:
        params = {
            "service": "https://www.douyin.com",
            "token": token,
            "need_logo": "false",
            "is_frontier": "false",
            "need_short_url": "false",
            # "passport_jssdk_version": "1.0.26",
            # "passport_jssdk_type":"pro",
            # "aid": 6383,
            # "language":"zh",
            # "account_sdk_source":"sso",
            # "account_sdk_source_info":"7e276d64776172647760466a6b66707777606b667c273f3433292772606761776c736077273f63646976602927666d776a686061776c736077273f63646976602927766d60696961776c736077273f63646976602927756970626c6b76273f302927756077686c76766c6a6b76273f5e7e276b646860273f276b6a716c636c6664716c6a6b762729277671647160273f2775776a68757127785829276c6b6b60774d606c626d71273f3c343429276c6b6b6077526c61716d273f32353629276a707160774d606c626d71273f3435363729276a70716077526c61716d273f343c3735292776716a64776260567164717076273f7e276c6b61607d60614147273f7e276c6167273f276a676f6066712729276a75606b273f2763706b66716c6a6b2729276c6b61607d60614147273f276a676f6066712729274c41474e607c57646b6260273f2763706b66716c6a6b2729276a75606b4164716467647660273f27706b6160636c6b60612729276c7656646364776c273f636469766029276d6476436071666d273f6364697660782927696a66646956716a77646260273f7e276c76567075756a77714956716a77646260273f717770602927766c7f60273f3131303535292772776c7160273f7177706078292776716a7764626054706a7164567164717076273f7e277076646260273f34303c36363c292774706a7164273f373c3c303532373137303c3d29276c7655776c73647160273f6364697660787829276b6a716c636c6664716c6a6b556077686c76766c6a6b273f2761606364706971272927756077636a7768646b6660273f7e27716c68604a776c626c6b273f34323737353d36313d373330332b312927707660614f564d606475566c7f60273f3737303c353532353429276b64736c6264716c6a6b516c686c6b62273f7e276160666a616061476a617c566c7f60273f343537303637362927606b71777c517c7560273f276b64736c6264716c6a6b2729276c6b6c716c64716a77517c7560273f276b64736c6264716c6a6b2729276b646860273f276d717175763f2a2a7272722b616a707c6c6b2b666a682a616c76666a73607727292777606b61607747696a666e6c6b62567164717076273f276b6a6b2867696a666e6c6b62272927766077736077516c686c6b62273f276c6b6b60772971715a6462722966616b286664666d602960616260296a776c626c6b272927627069605671647771273f3435313d2b363c3c3c3c3c3c3c3c3c35333c29276270696041707764716c6a6b273f276b6a6b602778782927776074706076715a6d6a7671273f277272722b616a707c6c6b2b666a68272927776074706076715a7564716d6b646860273f272a616c76666a736077277",
            # "passport_ztsdk": "3.0.20",
            # "passport_verify": "1.0.17",
            # "sdk_version":"2.2.7-beta.6",
            # "verifyFp": self.fp,
            # "fp": self.fp,
            # "device_platform":"web_app",
            # "msToken": self.msToken,
        }
        params.update({"a_bogus": self.a_bogus(params)})

        res = self.get(
            "https://sso.douyin.com/check_qrconnect/",
            params=params,
            headers={
                "Origin": "https://www.douyin.com",
                "Referer": "https://www.douyin.com/",
                "User-Agent": self.userAgent,
                "Bd-Ticket-Guard-Iteration-Version": "1",
                "Bd-Ticket-Guard-Ree-Public-Key": "BPIoN4LWKYuNIhARA8hb/VHl6qN4scB6YkWcKoP+jufHq7vofZiJU8EaOIAZFKb1gs/Og4S7SLDhGJPqNH5/V20=",
                "Bd-Ticket-Guard-Version": "2",
                "Bd-Ticket-Guard-Web-Version": "1",
                "X-Tt-Passport-Csrf-Token": self.passportCsrfToken,
            },
        )
        result: douyin.QrCheckRes = res.json()
        self.logger.debug("qrcode登录检查:{result}", result=result)
        if result["error_code"] != douyin.QrCheckErrorCode.Success.value:
            raise Exception(result.get("description") or "扫码登录失败")
        scanStatus = result.get("data").get("status")
        if scanStatus in [douyin.QrStatus.已扫码.value, douyin.QrStatus.已扫码2.value]:
            self.logger.debug("已扫码")
        elif scanStatus in [
            douyin.QrStatus.未扫码.value,
            douyin.QrStatus.未扫码2.value,
        ]:
            self.logger.debug("未扫码")
        elif scanStatus in [douyin.QrStatus.登录成功.value]:
            return result.get("data").get("redirect_url")

        #   得到ticket
        # 请求https://www.douyin.com/login/?next=https%3A%2F%2Fwww.douyin.com&ticket=337c287605d767929b8e66e579a14ace_lq
        # 重定向 https://www.douyin.com/passport/sso/login/callback/?ticket=337c287605d767929b8e66e579a14ace_lq&next=https%3A%2F%2Fww
        return

    def qrLogin(self, timeout: int = 60):
        retry = 1

        while retry:
            if self.passportCsrfToken:
                retry = 0
            params = {
                "service": "https://www.douyin.com",
                "need_logo": False,
                "is_frontier": False,
                "need_short_url": False,
                "device_platform": "web_app",
                "aid": 6383,
                "account_sdk_source": "sso",
                "sdk_version": "2.2.7-beta.6",
                "language": "zh",
                "verifyFp": self.fp,
                "fp": self.fp,
            }
            params.update({"a_bogus": self.a_bogus(params)})

            res = self.get(
                "https://sso.douyin.com/get_qrcode/",
                params=params,
                headers={
                    "Origin": "https://www.douyin.com",
                    "Referer": "https://www.douyin.com/",
                    "X-Tt-Passport-Csrf-Token": self.passportCsrfToken,
                },
            )
            if retry:
                continue

            result: douyin.QrLoginRes = res.json()
            self.logger.debug("检查数据:{result}", result=result)
            if result.get("error_code") != 0:
                self.logger.error("请求失败:{result}", result=result)
                return

        qrcode = result.get("data").get("qrcode")
        base64Img = base64.b64decode(qrcode)
        img = Image.open(BytesIO(base64Img))
        img.save("qrcode.png")
        os.system("start qrcode.png")

        token = result.get("data").get("token")

        while timeout > 0:
            jumpUrl = self.checkQr(token)
            if jumpUrl:
                res = self.get(jumpUrl)
                # https://www.douyin.com/passport/sso/login/callback/?ticket=641edbde938a422c6b81ba67c94fd2da_hl&next=https%3A%2F%2Fwww.douyin.com
                # 获取ticket直接登录
                print(res)
                return True
            time.sleep(1)
            timeout -= 1

        return False

    def qrLogin2(self):

        res = self.get(
            "https://sso.douyin.com/check_qrconnect/",
            params={
                "service": "",
                "token": "",
                "need_logo": False,
                "is_frontier": False,
                "need_short_url": False,
                "device_platform": "web_app",
                "aid": 6383,
                "account_sdk_source": "sso",
                "sdk_version": "2.2.7-beta.6",
                "language": "zh",
                "verifyFp": "",
                "fp": "",
                "msToken": "",
                "X-Bogus": "",
            },
        )

    def smsCheck(self, phone: str, verify_ticket: str):
        """发送短信验证码 登录校验
                response: {
            "data": {
                "mobile": "136******19",
                "mobile_ticket": "",
                "retry_time": 60
            },
            "message": "success"
        }"""
        params = {
            "new_authn_sdk_version": "1.0.21-web",
            "device_platform": "webapp",
            "msToken": self.msToken,
        }
        params.update({"a_bogus": self.a_bogus(params)})
        res = self.post(
            "https://www.douyin.com/passport/web/send_code/",
            params=params,
            data={
                "mix_mode": 1,
                "type": 3737,
                "is6Digits": 1,
                "verify_ticket": verify_ticket,
                "encrypt_uid": "",
                "aid": 6383,
                "new_authn_sdk_version": "1.0.21-web",
            },
        )

        resj = res.json()

    def verifySmsCode(self, verify_ticket: str, code: str):
        """验证短信验证码 登录校验
                response: {
            "data": {
                "captcha": "",
                "desc_url": "Please see https://zjsms.com/JqeFwYh/ for help",
                "description": "错误次数过多或验证码过期，请稍后重试",
                "error_code": 1203
            },
            "message": "error"
        }
        {
            "data": {
                "ticket": "VTIDEFMUGD7TWNSUKXSJEEG5XVJFN3EDXWKNPC_hl"
            },
            "message": "success"
        }"""
        params = {
            "new_authn_sdk_version": "1.0.21-web",
            "device_platform": "webapp",
            "msToken": self.msToken,
        }
        params.update({"a_bogus": self.a_bogus(params)})
        res = self.post(
            "https://www.douyin.com/passport/web/validate_code/",
            params=params,
            data={
                "mix_mode": 1,
                "type": 3737,
                "code": code,
                "verify_ticket": verify_ticket,
                "encrypt_uid": "",
                "aid": 6383,
                "new_authn_sdk_version": "1.0.21-web",
            },
        )

        resj = res.json()

    @property
    def ttwid(self):
        if not self.cookies.get("ttwid"):
            res = self.post(
                "https://ttwid.bytedance.com/ttwid/union/register/",
                json={
                    "region": "cn",
                    "aid": 1768,
                    "needFid": False,
                    "service": "www.ixigua.com",
                    "migrate_info": {"ticket": "", "source": "node"},
                    "cbUrlProtocol": "https",
                    "union": True,
                },
            )
            # res = self.get('https://www.douyin.com/user/MS4wLjABAAAA0joAdG_sxN6RJAXJBsXdzh1NzoVNYVgmhGYjooGY9t4',headers={
            #     'Referer': 'https://www.douyin.com/user/MS4wLjABAAAA0joAdG_sxN6RJAXJBsXdzh1NzoVNYVgmhGYjooGY9t4',
            # })
            # res = self.get('https://www.douyin.com/discover?modal_id=7352081640375553299')
            self.logger.debug(res.request.headers)

        ttwidStr = self.cookies.get("ttwid")
        if ttwidStr:
            return ttwidStr

        self.logger.error("获取ttwid失败")
        return ""

    def otherProfile(self, sec_user_id: str):
        """用户信息"""
        params = {
            **self.defaultParams(6, sec_user_id=sec_user_id),
            "verifyFp": self.fp,
            "fp": self.fp,
        }

        params.update({"a_bogus": self.a_bogus(params)})

        url = "https://www.douyin.com/aweme/v1/web/user/profile/other/"
        res = self.get(
            url,
            params=params,
            headers={
                "referer": f"https://www.douyin.com/user/{sec_user_id}",
                "User-Agent": self.userAgent,
            },
        )

        if len(res.content) <= 0:
            return

        data: douyin.ProfileOtherResType = res.json()

        return data
        # res = self.get(f'https://www.douyin.com/user/{sec_user_id}',headers={
        #     'referer': f'https://www.douyin.com/user/{sec_user_id}',
        #     'user-agent': self.userAgent,
        # })
        # data = re.findall(r'self\.__pace_f\.push\((.*?)\)',res.text,re.S)
        # try:
        #     data = json.loads(data[-1])
        #     data = data[1][2:]
        #     data = json.loads(data)
        #     data = data[-1]
        #     userInfo: douyin.HomePageUserInfoType = data['user']['user']

        #     return userInfo
        # except Exception as err:
        #     self.logger.error(err)
        #     return

    def videoList(self, sec_user_id: str):
        """作品列表
        API: max_cursor=0&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18
        """
        url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
        params = {
            "device_platform": "webapp",
            "aid": 6383,
            "sec_user_id": sec_user_id,
            "max_cursor": 0,
            "locate_query": "false",
            "show_live_replay_strategy": "1",
            "need_time_list": 1,
            "time_list_query": 0,
            "cut_version": 1,
            "count": 18,
            "msToken": self.msToken,
        }

        params.update({"a_bogus": self.a_bogus(params)})
        res = self.get(
            url,
            params=params,
            headers={"referer": f"https://www.douyin.com/user/{sec_user_id}"},
        )

        resj: douyin.AwemePostResType = res.json()

        return resj

    def videoMixList(self, sec_user_id: str):
        """用户作品合集列表"""

        url = "https://www.douyin.com/aweme/v1/web/mix/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAqUUm4EffFejs18KzTEf6qx-f4mYGLazKKgdGPVfzGO9fAAoNeTi9xrJw8VnLsvKx&req_from=channel_pc_web&cursor=0&count=12&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7353624324970219043"

    def videlLocateList(self, sec_user_id: str, max_cursor: int = 0):
        url = "https://www.douyin.com/aweme/v1/web/locate/post/"
        "locate_item_id=7338022829318819107&locate_item_cursor=1708516602000&locate_query=true"
        params = {
            "sec_user_id": sec_user_id,
            "max_cursor": max_cursor,
            "locate_item_id": "7338022829318819107",
        }
        res = self.get(url)

    def awemeCommentList(self, aweme_id: str, cursor=0, count=20):
        if not self.hasLogin:
            raise Exception("未登录")

        url = "https://www.douyin.com/aweme/v1/web/comment/list/"
        params = {
            # 'device_platform': 'webapp',
            # 'aid': 6383,
            # 'channel': 'channel_pc_web',
            # "aweme_id":aweme_id,
            # 'cursor': cursor,
            # 'count': count,
            # 'item_type': 0,
            # 'insert_ids': '',
            # 'whale_cut_token': '',
            # 'cut_version': 1,
            # 'pc_client_type': 1,
            # 'webid': self.webid,
            # 'msToken': self.msToken,
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "aweme_id": "7396387923278449955",
            "cursor": "20",
            "count": "20",
            "item_type": "0",
            "insert_ids": "",
            "whale_cut_token": "",
            "cut_version": "1",
            "rcFT": "",
            "update_version_code": "170400",
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "126.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "126.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "16",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "10",
            "effective_type": "4g",
            "round_trip_time": "100",
            "webid": self.webid,
            # "msToken": '6ny6Bz8aqiMMh5yH6qOWUrNbQMgFQBlN1Pes1-IEkyIcQYOq0lKDPxC54E-6O0pPp31ZtbfsQOe9YvO9n61GPsOw5s7dih7UuMnMvM80JVCOmIwuGZCs',
            "msToken": 'dbk_l4hM49TG3_9-AobdX2H2O7ffUmRdhDVXSSoHi5eajBAwR2kCOU2X7EDoAL9bDY1eHxcoGlYf1O_2YPKE3IzIJKpCcvXuWB3UoVAivwzctyLvzS6-',
            # 'verifyFp': self.fp,
            # 'fp': self.fp,
        }

        params.update({"a_bogus": self.a_bogus(params)})

        res = self.get(
            url,
            params=params,
            headers={
                "referer": "https://www.douyin.com/",
                "host": "www.douyin.com",
                "user-agent": self.userAgent,
            },
        )
        # print(res.request.headers)
        #   错误返回
        #   {"status_code":5,"status_msg":"","log_pb":{"impr_id":"202404042053520DD3E00E46C79CCA6D42"}}
        resp: douyin.VideoCommentType = res.json()
        # self.renderType('UserMini', resp['comments'][0]['user'])

        return resp

    def queryUserInfo(self, sec_user_id: str):
        url = "https://www.douyin.com/aweme/v1/web/im/user/info/"
        params = {
            **self.defaultParams(1),
        }

        res = self.post(
            url,
            params=params,
            data={"sec_user_ids": [sec_user_id]},
            headers={
                "referer": f"https://www.douyin.com/user/{sec_user_id}",
                "X-Secsdk-Csrf-Token": self.domain_token(url),
            },
        )
        resp = res.json()

    def hotSearchList(self):
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&main_billboard_count=5&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7353624324970219043"

    def search(self, keyword: str, offset: int = 0, count: int = 12):
        url = "https://www.douyin.com/aweme/v1/web/discover/search/"
        params = {
            "search_channel": "aweme_user_web",
            "keyword": keyword,
            "search_source": "normal_search",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "offset": offset,
            "count": count,
            "need_filter_settings": 1,
        }

        res = self.get(url, params=params)

        resp = res.json()

    def report(self):
        res = self.post(
            "https://mssdk.bytedance.com/web/report",
            params={
                "msToken": self.msToken,
                "X-Bogus": "",
            },
            headers={"cookie": f"msToken={self.msToken}"},
        )
        # print(res)

    def check(self):
        res = self.get(
            "https://tnc3-bjlgy.zijieapi.com/get_domains/v5/",
            params={
                "tnc_js_sdk_version": "2.1.0.0",
                "device_platform": "pc",
                "aid": "6383",
                "device_id": self.webid,
                "web_service": "",
            },
        )
        print(res.json())

    def renderType(self, name: str, params: Any):
        if not isinstance(params, dict):
            return

        params_type_template = """
class {name}Type(TypedDict):
{paramsStr}
"""

        paramsStr = ""
        for key in params:
            paramsStr += f"    {key}: {self.typeStr(params[key])}\n"

        douyinTypePath = Path(__file__).parent.parent.joinpath("types/douyin.py")
        with open(douyinTypePath, "a+", encoding="utf-8") as f:
            f.write(params_type_template.format(name=name, paramsStr=paramsStr))

    def getDeviceInfoParams(self):
        common_search_params = {
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
        }
        return {
            "version_code": "290100",
            "version_name": "29.1.0",
            "os": "web",
            "device_brand": "web",
            "device_model": "web",
            "device_type": "web_device",
        }

    def getNavigatorParams(self):
        return {
            "cookie_enabled": True,
            "screen_width": 1920,
            "screen_height": 1080,
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "123.0.0.0",
            "browser_online": True,
            "engine_name": "Blink",
            "engine_version": "123.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": 16,
            "device_memory": 8,
            "platform": "PC",
            "downlink": 10,
            "effective_type": "4g",
            "round_trip_time": 50,
        }

    def getCsrfToken(self, domain: str, path: str) -> douyin.WareCsrfToken:
        """获取csrftoken"""
        if not domain.startswith("https://"):
            domain = f"https://{domain}"

        res = self.head(
            f"{domain}{path}",
            headers={
                # 'x-secsdk-csrf-request': '1',
                # 'x-secsdk-csrf-version': '1.2.22',
                **self.douyinSecsdkHeader
            },
        )
        if res.status_code != 200:
            raise Exception("获取token失败")

        headerVal = res.headers.get("x-ware-csrf-token")
        if not headerVal:
            raise Exception("获取csrf token失败")

        tokenValid, token, maxAge, *other = headerVal.split(",")
        if tokenValid != "0":
            raise Exception(f"错误的数值:{headerVal}")

        return {
            "value": token,
            "expiredAt": int(time.time() * 1000) + int(maxAge),
            "timeout": False,
        }

    def queryUser(self):
        url = "https://www.douyin.com/aweme/v1/web/query/user/?device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=126.0.0.0&browser_online=true&engine_name=Blink&engine_version=126.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7396557428572259851&verifyFp=verify_lz54tc0u_SBhVS6ay_l5yx_4uUx_BZur_uIAdQ6bGxnVz&fp=verify_lz54tc0u_SBhVS6ay_l5yx_4uUx_BZur_uIAdQ6bGxnVz&a_bogus=QfWMQfufmDdsgf6X51%2FLfY3q6lp3YD5Y0trEMD2f%2FV3Geg39HMOO9exoRmkv0dujNs%2FDIeYjy4hCYpqMx5AJA3vRHuDKUIcgmESkKl5Q5xSSs1Xce6UgrUkE-wsACFrQsv1lxOfkohAbSY8DAxAJ5kIlO62-zo0%2F9XS%3D"


"""
这3个cookie才能请求到数据
sid_tt=876ef0e20d
sessionid=876ef0
sessionid_ss=876e
sid_guard   重要

{"s0":"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=","s1":"Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=","s2":"Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=","s3":"ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe","s4":"Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"}
"""
