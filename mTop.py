# coding:utf-8
try:
    from .taobao.淘宝H5 import TB_H5
    from .taobao.淘宝开放平台 import TB_openPlatform
    from .taobao.SDK基类 import Base
    from .util.tools import BackThread
except ImportError as e:
    from taobao.淘宝H5 import TB_H5
    from taobao.淘宝开放平台 import TB_openPlatform
    from taobao.SDK基类 import Base

    from util.tools import BackThread

import json
# from threading import Thread
from time import sleep,strftime,time
from requests.cookies import RequestsCookieJar
from urllib.parse import urljoin,parse_qsl,urlparse,quote
from collections import OrderedDict
import re
from lxml import etree
import math
from ctypes import c_uint32,c_int32
from random import random

class Client(Base):

    def __init__(self):
        super(Client,self).__init__()
        self.H5 = TB_H5()
        self.open = TB_openPlatform()
        self.setcookie()
    
    # def __first(self,domain:str='https://h5api.m.taobao.com',url:str="/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
    #     '''
    #         必须首先请求一个api来获取到h5token
    #         有多个API时，需要先获取多个API下面的token
    #         如果是https://h5api.m.tmall.com下的API也是需要先获取token的
    #     '''
    #     res = self.get(urljoin(domain,url))
    #     return res

    def setcookie(self):
        _uab_collina = ''
        for i in range(20):
            if len(_uab_collina) < 11:
                _uab_collina += str(random())[2:]
            else:
                break
        #第一个cookie,domain为login.taobao.com，path为/member
        _uab_collina = str(int(time() * 1000)) + _uab_collina[len(_uab_collina) - 11:]
        self.H5.cookies.set('_uab_collina',_uab_collina,domain='login.taobao.com',path='/member')

        #第二个cookie，请求这个JS，https://log.mmstat.com/eg.js，然后把etag的值设置为cna
        res = self.H5.get('https://log.mmstat.com/eg.js')
        cna = re.findall(r'Etag="(.*?)"',res.text)[0]
        self.cookies.set('cna',cna,domain='.taobao.com',path='/')

        #第三个cookie，isg为算法生成的，不好破解，domain为.taobao.com，path为/
        isg = 'BM3NGuFcrQh-tgkk_KLDk9jr3OlHqgF8pnooOQ9SCWTTBu241_oRTBuUcNrFxhk0'
        self.H5.cookies.set('isg',isg,domain='.taobao.com',path='/')

        #第四个cookie，l为算法生成,domain为.taobao.com，path为/
        l = 'bBgKwFjlv-QtIl3JBOCanurza77OSIRYYuPzaNbMi_5pK6T_Bk7OlgnjDF96Vj5RsxYB4-L8Y1J9-etkZ'
        self.H5.cookies.set('l',l,domain='.taobao.com',path='/')  
    
    def login(self,umid_token,domain:str='https://www.taobao.com'):
        self.defaulturl = domain
        # self.H5.get(f'https://login.taobao.com/member/login.jhtml?redirectURL={domain}')
        self.H5.get(f'https://login.taobao.com/member/login.jhtml?allp=&wbp=&sub=false&sr=false&c_is_scure=&from=tbTop&type=1&style=&minipara=&css_style=&tpl_redirect_url={quote(domain)}&popid=&callback=&is_ignore=&trust_alipay=&full_redirect=&need_sign=&sign=&timestamp=&from_encoding=&qrLogin=&keyLogin=&newMini2=')
        res = self.H5.get(f'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={umid_token}')
        # data = json.loads(res.text)
        # thd = self.checkState(data['lgToken'],umid_token,timeout)
        return res
    
    def checkState(self,lgToken,umid_token,timeout):
        '''在闭包中修改变量要使用nonlocal关键字'''
        def run():
            nonlocal timeout
            # locals()['lgToken'] = lgToken
            # locals()['umid_token'] = umid_token
            # locals()['timeout'] = timeout
            # print(lgToken)
            while timeout > 0:
                self.H5.headers.update({
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                            'Referer':'https://login.taobao.com/member/login_unusual.htm?user_num_id=2979250577&is_ignore=&from=tbTop&style=&popid=&callback=&minipara=&css_style=&is_scure=true&c_is_secure=&tpl_redirect_url=https%3A%2F%2Fwww.taobao.com%2F&cr=https%3A%2F%2Fwww.taobao.com%2F&trust_alipay=&full_redirect=&need_sign=&not_duplite_str=&from_encoding=&sign=&timestamp=&sr=false&guf=&sub=false&wbp=&wfl=null&allp=&loginsite=0&login_type=11&lang=zh_CN&appkey=00000000&param=7nmIF0VTf6m%2Bbx8wuCmPLTEdh1Ftef8%2B5yUA%2FXNtAI%2FfMwadkeaCast40u2Ng0%2FC7Z75sOSVLMugWTqKjJ7aA55JYIL%2FPDFJ7zaJhq9XSVUOX%2B1AxQatuIvw4TXGJm1VG4alZ2UohVAAt5WTLYbs5im077nTG%2BOkovORQNtMCEzWKMe0xcuienFAhsBhC0V7qIYZJvPGOOEt0tORA8Fv1zYPuOkWEPDFsPwYG5xj4LTKNZt5HSRRHkviiPy9AJ9uC%2Bs7V%2FQ7b6K07YUG1fA3tFwALGnorSUXRdhcXUBBAt6IiyStIkWFWDgJEymOAXOS5RNGlO1EL5ppmpQas7BarrW2Krui4bxV81AJXyxLfnk3MOxI2dUNdO9VQNY0F6a6nk%2FCzUfR0NfPRrIoXuZDn2N01A8q5XGrMlWmBCH5%2FSKz6%2F%2BrUx3%2FxQTYWmgV49rVSdtySIHip5PsrXHWXCbHqscdve540l5CUKTT7znsoL45pth%2FosxMUb649Yw1EPAq'
                        })
                res = self.H5.get(f'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={lgToken}&defaulturl={self.defaulturl if hasattr(self,"defaulturl") else "www.taobao.com"}')
                data = json.loads(res.text)
                if data['code'] == '10006':
                    print(data)
                    url = data['url'] + '&umid_token=' + umid_token
                    res_main = self.H5.get(url)
                    print('扫码成功')
                    if res_main.url.find('login_unusual.htm') > -1:
                        return False
                        # URL = re.findall(r"url:'(.*?)',",res_main.text)[0] if re.findall(r"url:'(.*?)',",res_main.text) else None
                        # if not URL:
                        #     status = False
                        # res = self.H5.get(URL)
                        # txt = res.text.replace(re.findall(r'''"tipsInfo":".*?",''',res.text)[0],'')
                        # data = json.loads(re.findall(r"value='(.*?)'",txt)[0])
                        # param = data.get('param')
                        # target = data.get('options')[0]['optionText'][0]['code']
                        # self.H5.headers.update({'Origin':'https://aq.taobao.com','Referer':'https://aq.taobao.com/durex/validate?param=7nmIF0VTf6m%2Bbx8wuCmPLV6h%2FBQmDRI8eV0OZyuo1fwa%2FgvJ5VoYvhtsoSv%2BF6cVUYizmLOxpLs2mfNAJ8vsGbcBnf0mzB1xSKqsSGvUqY%2Bq5%2FxX1gBcxe0gF0LFtAmr%2FWJFjntGTKMrtyIKbwf5ouytcdZcJseqVq8v%2Fy9%2FeTX4wWc9LeLhPtz8D7l%2FxF%2BCIJggV7kbXlu7mGPRB7pECo%2B2ziHSK%2BByv5YxyYP2zNhUh4QXk5GvHVwJW%2Bua9aMJPAoVN5qoDgqHkrh2z5WYxiZzWy%2BtzWY2652vDwnjI%2F1O7f%2BQy7nknGS71GKCQqOGs3AMkiRA4F2Fhe5TrpbLcH6HfmPw4xL2Y%2BTM1%2F6RVEHcLNdcER2hJ89lHMKhuywTXjzIEiEJAa7NzBo6GJAS2iAUs1CRfB5KaLZHD%2FA1QCQQXiS%2F8FgFVV%2FnCMMCninEOgC%2FLnlUcHBCWBb8kdeKUOAQKft0cdJbKwTKZRdNvxGePGPRtvDX%2Bk7xAUDsqTuPoR6d2gik3XA8G1nKKH%2BEZ8lneUmpZXuM0t1kVDQM4qYfrTw3yLxh6g%3D%3D&redirecturl=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin_mid.htm','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
                        # res = self.sendcode(param,target)
                        # code = ''
                        # res = self.checkcode(param,code,target)
                        # urls = re.findall(r'"(.*?login_by_safe.htm.*?)"',res_main.text)
                        # print(urls)
                        # res = self.H5.get(urls[1])
                        # dt = OrderedDict(parse_qsl(URL.query))
                        
                        # res2 = self.H5.get(f'https://aq.taobao.com/durex/validate?param={dt["param"]}&redirecturl=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin_mid.htm')
                        # print(res2.url)
                        print('需要安全验证登录')
                    return True
                    break
                elif data['code'] == '10001':
                    print('正在扫码')
                    sleep(1)
                    continue
                elif data['code'] == '10004':
                    timeout = 0
                    break
                elif data['code'] == '10000':
                    # print(data['message'])
                    pass
                timeout -= 1
                sleep(1)
            return False
        
        # thd = Thread(target=run)
        thd = BackThread(run,())
        return thd

    def sendcode(self,param:str='',target=''):
        domain = 'https://aq.taobao.com/durex/sendcode'
        data = {
            'checkType':'phone',
            'target':target,
            'safePhoneNum':'',
            'checkCode':''
        }
        res = self.H5.post(domain,params={'param':param,'checkType':'phone'},data=data)
        
        try:
            data = json.loads(res.text)
            print(data.get('message') or '发送失败')
        except Exception as e:
            print(res.text)
        return res
    
    def checkcode(self,param,code,target):
        head = {'origin':'https://aq.taobao.com'}
        domain = 'https://aq.taobao.com/durex/sendcode'
        data = {
            'checkType':'phone',
            'target':'',
            'safePhoneNum':'',
            'checkCode':code,
            'pageLog':{
                'actions':[
                    {'result':'true','target':'其他验证方式','targetType':'a','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'},
                    {'result':'true','target':'手机短信验证','targetType':'div','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'},
                    {'result':'true','target':'确定','targetType':'button','attr':'','userTime':strftime('%Y-%m-%d %H:%M:%S'),'type':'operation'}
                ]
            }
        }
        res = self.H5.post(domain,params={'param':param},data=data)
        try:
            data = json.loads(res.text)
            print(data.get('message') or '发送失败')
        except Exception as e:
            print(res.text)
        return res

    def sendMsg(self,phone,url:str='https://login.m.taobao.com/sendMsg.do',domain:str='https://h5.m.taobao.com'):
        um_token = self.um_token if hasattr(self,'um_token') else self.get_umtoken()
        if um_token:
            self.um_token = um_token
        form = {
            'TPL_username':phone,
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'',
            'um_token':um_token,
            'ua':'115#1XACqf1O1TZSLM6AtfGU1CsoE5sZIpA11g2u11XZKC11q8V4OODHhSThyzrO8jmUbA38uRKQi/rKyf/PAihcaLpXyrPQAS5yetT4ykNpi/buxEONAWNcaT6burPQvIAbAXlCuWZQ8bWRhUFGAWNcaLIEyrrQOSAPe1L8ykNQOQk5hEz4ioYR/n9jsOC/PtMQSFAFFKjH17QffqcKLpRdI0a+LgqiNyGDJD3ZJU4nL4ya7RsqspO5kK6Ld+eYL32W564xY3sQIo3tD4EGIfZxPeNsYCQoAvHUQDZ3FJgmIMl1L9h4uNsyN1h7M9OxElI99jJ5RLqBSZrZo+2XyCJlP+JmgUIIWC9P6e2MiOzsQKtUasFuk7dAEx3SCFOWQekLbUqN4joU9XsOuORJ+NvOZodes1q87cN7NjhAvZBYkimei6Ef8a6CcWAlcVxY4lrVvL2GBsk/KX5WzSsFczSy8o/OovaGNGQIXWqhEmNWtQEG/UO3BbjYvcoiiTZFD5NWs4jfyYdVLvj9z3dCYokpucjezXGarYssy6yTPIR1LAp0TDZQkD9xvAEYLHdHRhhSfy5cgtPb/Z9ciDQZaOlOxBZfxO2tUmcJSFmIzwA854e0dv9fDuJkO9Ot65ThGbW53+i1qwcJ3kqmLFzl/1IgOZJjdTaZxmeeRvoA6l45slMvpKdEx0dG3qwDRYdPdpMpSCfW0ekrB9YssLumV0miZO5EPZzR'
        }
        res = self.H5.post(url,form)
        print(res.text)
        data = json.loads(res.text)
        return data

    
    def msgForm(self,phone:str,sms_code:str,options:dict={}):
        url = 'https://login.m.taobao.com/msg_login.htm'
        
        form = {
            'TPL_username':phone,
            'msgCheckCode':sms_code,
            'otherLoginUrl':'https://login.m.taobao.com/login.htm?nv=true&spm=0.0.0.0&ttid=h5%40iframe&redirectURL=https%3A%2F%2Fh5.m.taobao.com',
            'action':'MsgLoginAction',
            'event_submit_do_login':1,
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'',
            'TPL_redirect_url':'https://h5.m.taobao.com',
            'loginFrom':'WAP_TAOABO',
            'smsTime':'',
            'smsToken':'',
            'page':'msgLoginV3',
            'um_token':self.um_token if hasattr(self,'um_token') else self.get_umtoken(),
            # 'ua':''
        }

        if options:
            form.update(options)
        
        res = self.H5.post(url,data=form,params={'spm':'','ttid':'h5@iframe','redirectURL':'https://h5.m.taobao.com/other/loginend.html?origin=https%3A%2F%2Fmain.m.taobao.com'})
        print(res.text)
        return res

    def getUid(self,url:str='https://ynuf.alipay.com/uid'):
        '''获取的缓存id'''
        res = self.H5.get(url)
        print(res.text)
        try:
            cid = res.text[11:-3]
        except Exception:
            cid = ''
        return cid

    def encrypt(self,code):
        n = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        s = ''
        l = 0
        while l < len(code):
            try:
                t = ord(code[l])
            except IndexError as e:
                t = 0# t = math.nan
            l += 1
            try:
                r = ord(code[l])
            except IndexError as e:
                r = 0 # r = math.nan
            l += 1
            try:
                i = ord(code[l])
            except IndexError as e:
                i = 0 # i = math.nan
            l += 1
            o = t >> 2
            a = (3 & t) << 4 | r >> 4
            # if type(r) or type(i) == 'float':
            #     print(r,i)
            u = (15 & r) << 2 | i >> 6
            c = 63 & i
            if r == 0:
                u = c = 64
            else:
                c = 64 if i == 0 else c
            s = s + n[o] + n[a] + n[u] + n[c]
            # print(s)
        return s
    
    #这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算
    def int_overflow(self,val):
        maxint = 2147483647
        if not -maxint-1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val
    
    def unsigned_right_shitf(self,n,i):
        # 数字小于0，则转为32位无符号uint
        if n<0:
            n = c_uint32(n).value
        # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
        if i<0:
            return -self.int_overflow(n << abs(i))
        #print(n)
        return self.int_overflow(n >> i)
    
    def left_move(self,a,bit):
        return c_int32(a << bit).value

    def ROTL(self,e,t):
        return self.left_move(e,t) | self.unsigned_right_shitf(e,32 - t)
    
    def toHexStr(self,e):
        n = ''
        for r in range(7,-1,-1):
            t = c_int32(self.unsigned_right_shitf(e,4 * r)).value & c_int32(15).value
            n += hex(t)[2:]
        return n
    
    def f(self,e,t,n,r):
        '''这里的值计算出来好像没有问题，但是为什么会没有问题？'''
        if e == 0:
            return t & n ^ ~t & r
        elif e == 1:
            return t ^ n ^ r
        elif e == 2:
            return t & n ^ t & r ^ n & r
        elif e == 3:
            return t ^ n ^ r
        

    def hash_encrypt(self,code,status=False):
        if not status:
            code = self.encrypt(code)
        
        r = [1518500249, 1859775393, 2400959708, 3395469782]
        code += chr(128)
        u = len(code) / 4 + 2
        c = math.ceil(u / 16)
        s = [None] * c
        for i in range(c):
            s[i] = [None] * 16
            for a in range(16):
                try:
                    _a = self.left_move(ord(code[64 * i + 4 * a]),24)
                except IndexError:
                    _a = 0
                try:
                    _b = self.left_move(ord(code[64 * i + 4*a + 1]),16)
                except IndexError:
                    _b = 0
                try:
                    _c = self.left_move(ord(code[64 * i + 4 * a + 2]),8)
                except IndexError:
                    _c = 0
                try:
                    _d = ord(code[64 * i + 4 * a + 3])
                except IndexError:
                    _d = 0

                s[i][a] = _a | _b | _c | _d
        s[c - 1][14] = 8 * (len(code) -1) / math.pow(2,32)
        s[c - 1][14] = math.floor(s[c - 1][14])
        s[c - 1][15] = 8 * (len(code) - 1) & 4294967295
        m = 1732584193
        g = 4023233417
        v = 2562383102
        T = 271733878
        S = 3285377520
        C = [None] * 80
        for i in range(c):
            for o in range(16):
                C[o] = s[i][o]
            for o in range(16,80):
                C[o] = self.ROTL(C[o -3] ^ C[o - 8] ^ C[o - 14] ^ C[o - 16],1)
            l = m
            f = g
            d = v
            p = T
            h = S
            for o in range(80):
                y = math.floor(o / 20)
                B = self.ROTL(l,5) + self.f(y,f,d,p) + h + r[y] + C[o] & 4294967295
                h = p
                p = d
                d = self.ROTL(f,30)
                f = l
                l = B
            m = c_int32(m + l).value & c_int32(4294967295).value
            g = c_int32(g + f).value & c_int32(4294967295).value
            v = c_int32(v + d).value & c_int32(4294967295).value
            T = c_int32(T + p).value & c_int32(4294967295).value
            S = c_int32(S + h).value & c_int32(4294967295).value
        
        return self.toHexStr(m) + self.toHexStr(g) + self.toHexStr(v) + self.toHexStr(T) + self.toHexStr(S)

    def get_umtoken(self,url='https://ynuf.aliapp.org/service/um.json'):
        '''获取um_token'''
        #获取cna的cookie值
        res = self.H5.get('https://log.mmstat.com/eg.js')
        res = self.H5.post(url,data={'data':'105!QRe+7JxkF0+z9g+NM+Zhkr0M+V9Qjt9QySeq3E9xKaIqgcHV5c4fMqPC7yFcGLV4JQXfZTXVr4A7ognGVuZ1t0s1zgKdL+m7FeEnzG01lmDDYuByVOE7t0s1zgKBg/skF0Eyzl2MiDmDyaLzKlVVz4ffTWCT5j6wnnDLX8Srdp0S325GCcfthSJkabDcR/7SZV6OB8sd4mhlX3B8tf7rnLmWCnYkVw2aZubW3CtvdpHwBX+1aBvjN7L2CnxeKdjAybxzuBnfGZLGPqNzW3YfC85+eqfz+RxKDftMNSeSo88KyK0xamV4HOiRjavjbRVevPEjqRG9vwmXOBiMHbudYp8Dp57df5voWLBMP1fMEfJdKuZ/U9vY+mP9T4CUvrfWitJFmrtzLw2Sll9YGz+fRfcx6nDYJumwkZU8ngMWt70U/4cKabPmKg84+PyyKI7wFBo4b1VKktrPHon9iDxD2KHQLnuMlQvAynQPB7GTKAZQ0dT8MNnl8DGBo8xIPbLwCWRgGsgdaZQG0R0QhqcTVbweZOlPIXH/PByHPAQi9H1YQg=='})
        psdata = json.loads(res.text)

        data = {
            'etf':'',
            'xa':'',
            'siteId':'',
            'uid':'',
            'eml':'AA',
            'etid':'',
            'esid':'',
            'bsh':398,
            'bsw':360,
            'cacheid':self.getUid(),
            'eca':self.H5.cookies.get('cna',''),
            'ecn':"0853e2dc2b17946f6cf315e412fb6b40a4aa9ec7",
            'eloc':'https%3A%2F%2Flogin.m.taobao.com%2Fmsg_login.htm',
            'ep':self.hash_encrypt(''),
            'epl':0,
            'epls':'',
            'esid':'',
            'esl':False,
            'est':2,
            'etf':'b',
            'etid':'',
            'ett':int(time() * 1000),
            'etz':480,
            'ips':'',
            'ms':'445388',
            'nacn':'Mozilla',
            'nan':'Netscape',
            'nce':True,
            'nlg':'zh-CN',
            'plat':'Win32',
            'sah':640,
            'saw':360,
            'sh':640,
            'sw':360,
            'type':'pc',
            'uid':'',
            'xs':'',
            'xt':self.getUmidToken(),
            'xv':'3.3.7'
        }
        res = self.H5.post(url,data={'data':'ENCODE~~V01~~' + self.encrypt(json.dumps(data))})
        print(res.text)
        _id = json.loads(res.text)
        self.H5.cookies.set('umdata_',_id.get('id'),domain='login.m.taobao.com',path='/')
        return _id.get('tn','')

if __name__ == '__main__':
    
    top = Client()
    # umid_token = top.getUmidToken()
    # res = top.login(umid_token)
    # print(res.text)
    # # cookie = {
    # #     '.login.taobao.com':top.cookies.get_dict('.login.taobao.com'),
    # #     '.taobao.com':top.cookies.get_dict('.taobao.com')
    # # }
    # # jar = RequestsCookieJar()
    # # for domain in cookie:
    # #     for name in cookie[domain]:
    # #         jar.set(name,cookie[domain][name],path='/',domain=domain)
    # # top.H5.cookies.update(jar)
    # data = json.loads(res.text)
    # thr = top.checkState(data['lgToken'],umid_token,120)
    # thr.start()
    # res = thr.get_result()
    # print(res)
    # top.H5.headers = {
    #     'Referer':'https://s.m.taobao.com/h5?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&q=%E7%94%B7%E8%A3%85',
    #     'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0; MI 4S MIUI/8.9.13)'
    # }
    phone = input('请输入手机号：')
    smsdata = top.sendMsg(phone)
    if smsdata.get('success'):

        smscode = input('请输入验证码：')
        res = top.msgForm('15623143699',smscode,{'smsTime':smsdata.get('smsTime'),'smsToken':smsdata.get('smsToken')})
    else:
        print(smsdata.get('message'))
    # res = top.encrypt('{"xv":"3.3.7","xt":"1554269482354:0.19720084919117342","etf":"b","siteId":"","uid":"","eml":"AA","etid":"","esid":"","type":"pc","nce":true,"plat":"Win32","nacn":"Mozilla","nan":"Netscape","nlg":"zh-CN","sw":360,"sh":640,"saw":360,"sah":640,"bsw":360,"bsh":398,"eloc":"https%3A%2F%2Flogin.m.taobao.com%2Fmsg_login.htm","etz":480,"ett":1554269537487,"ecn":"0853e2dc2b17946f6cf315e412fb6b40a4aa9ec7","eca":"KDMrFd7kz1kCAd3qgh/fqiQL","cacheid":"dc37a77d8019b693","xh":"","ips":"","epl":0,"ep":"da39a3ee5e6b4b0d3255bfef95601890afd80709","epls":"","esl":false}')
    # print(res)
    # res = top.hash_encrypt('')
    # print(res)
    res = top.H5.execute({
        'api':'mtop.taobao.alistar.dimensions.getData',
        'v':'1.0',
        'jsv':'2.4.2',
        'type':'json',
        'dataType':'jsonp',
        'data':{
            'ids':json.dumps({'dimensions':[0,1,2,3]},separators=(',',':'))
        }
    })
    print(res.text)
    # top.H5.config['domain'] = 'https://h5api.m.taobao.com'
    # res = top.H5.execute({
    #     'api':'mtop.taobao.geb.shopinfo.queryshopinfo',
    #     'v':'2.0',
    #     'jsv':'2.4.2',
    #     'dataType':'json',
    #     'type':'originaljson',
    #     'AntiCreep':'true',
    #     'H5Request':'true',
    #     'data':{
    #         'sellerId':2248971852
    #     }
    # });
    # print(res.text)
    # res = top.H5.execute({
    #     'api':'mtop.taobao.mclaren.getUserProfile',
    #     'v':'1.0',
    #     'jsv':'2.4.2',
    #     'type':'originaljson',
    #     'dataType':'originaljsonp',
    #     'isSec':1,
    #     'jsonpIncPrefix':'weexcb',
    #     'ttid':'2019@weex_h5_0.12.11',
    #     'data':{}
    # })
    # print(res.text)
    # top.H5.config['domain'] = 'https://api.m.taobao.com'
    # top.H5.config['domain'] = 'https://h5api.m.tmall.com' #需要先获取旗下的token
    # top.H5.config['path'] = 'rest/h5ApiUpdate.do'
    # res = top.H5.execute({
    #     'api':"mtop.d4s.service.ExternalizationService.queryStarLevel",
    #     'v':'1.0',
    #     'type':'json',
    #     'dataType':'jsonp',
    #     'ecode':1,
    #     'data':{
    #         'bid':1004827,
    #         'vid':'f17e4f92ddeee7d2d89eaf1936f806c2'
    #     }
    # })
    # print(res.text)
    # res = top.H5.execute({
    #     'api':'mtop.vip.gold.user.customize',
    #     'v':'1.0',
    #     'jsv':'2.4.2',
    #     'type':'json',
    #     'dataType':'jsonp',
    #     'timeout':20000,
    #     'data':{
    #         'source':'club'
    #     }
    # })
    # print(res.text)