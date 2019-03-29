# coding:utf-8
try:
    from .taobao.淘宝H5 import TB_H5
    from .taobao.淘宝开放平台 import TB_openPlatform
    from .taobao.SDK基类 import Base
except ImportError as e:
    from taobao.淘宝H5 import TB_H5
    from taobao.淘宝开放平台 import TB_openPlatform
    from taobao.SDK基类 import Base

import json
from threading import Thread
from time import sleep,strftime,time
from requests.cookies import RequestsCookieJar
from urllib.parse import urljoin,parse_qsl,urlparse
from collections import OrderedDict



class Client(Base):

    def __init__(self):
        super(Client,self).__init__()
        self.H5 = TB_H5()
        self.open = TB_openPlatform()
    
    # def __first(self,domain:str='https://h5api.m.taobao.com',url:str="/h5/mtop.taobao.wireless.home.load/1.0/?appKey=12574478"):
    #     '''
    #         必须首先请求一个api来获取到h5token
    #         有多个API时，需要先获取多个API下面的token
    #         如果是https://h5api.m.tmall.com下的API也是需要先获取token的
    #     '''
    #     res = self.get(urljoin(domain,url))
    #     return res
    
    def login(self,umid_token,domain:str='www.taobao.com'):
        self.defaulturl = domain
        self.H5.get(f'https://login.taobao.com/member/login.jhtml?redirectURL={domain}')
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
                    res = self.H5.get(url)
                    print('扫码成功')
                    if res.url.find('login_unusual.htm') > -1:
                        # URL = urlparse(res.url)
                        # dt = OrderedDict(parse_qsl(URL.query))
                        
                        # res2 = self.H5.get(f'https://aq.taobao.com/durex/validate?param={dt["param"]}&redirecturl=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin_mid.htm')
                        # print(res2.url)
                        print('需要安全验证登录')
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
        
        thd = Thread(target=run)
        return thd

    def sendcode(self,param:str='',target=''):
        domain = 'https://aq.taobao.com/durex/sendcode'
        data = {
            'checkType':'phone',
            'target':'',
            'safePhoneNum':'',
            'checkCode':''
        }
        res = self.H5.post(domain,params={'param':param})
        print(res.text)
    
    def checkcode(self,param,code,target):
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
        print(res.text)





if __name__ == '__main__':
    
    top = Client()
    umid_token = top.getUmidToken()
    res = top.login(umid_token)
    print(res.text)
    # cookie = {
    #     '.login.taobao.com':top.cookies.get_dict('.login.taobao.com'),
    #     '.taobao.com':top.cookies.get_dict('.taobao.com')
    # }
    # jar = RequestsCookieJar()
    # for domain in cookie:
    #     for name in cookie[domain]:
    #         jar.set(name,cookie[domain][name],path='/',domain=domain)
    # top.H5.cookies.update(jar)
    data = json.loads(res.text)
    thr = top.checkState(data['lgToken'],umid_token,30)
    thr.start()
    thr.join()

    # top.H5.headers = {
    #     'Referer':'https://s.m.taobao.com/h5?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&q=%E7%94%B7%E8%A3%85',
    #     'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0; MI 4S MIUI/8.9.13)'
    # }

    # res = top.H5.execute({
    #     'api':'mtop.taobao.alistar.dimensions.getData',
    #     'v':'1.0',
    #     'jsv':'2.4.2',
    #     'type':'json',
    #     'dataType':'jsonp',
    #     'data':{
    #         'ids':json.dumps({'dimensions':[0,1,2,3]},separators=(',',':'))
    #     }
    # })
    # print(res.text)
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