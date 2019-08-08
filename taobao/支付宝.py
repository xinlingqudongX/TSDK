
import requests
import re
from json.decoder import JSONDecodeError

try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base

class Alipay(Base):

    def __init__(self,head={
        'user-agent':'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 4S Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.18.0.54 Mobile Safari/537.36 UCBS/3.18.0.54_190719203139 NebulaSDK/1.8.100112 Nebula AlipayDefined(nt:WIFI,ws:360|0|3.0) AliApp(AP/10.1.68.7434) AlipayClient/10.1.68.7434 Language/zh-Hans useStatusBar/true isConcaveScreen/false Region/CN',
    }):
        super().__init__()
        # post
        self.login_url = 'https://auth.alipay.com/login/h5Login.json'
        self.smsToken_url = 'https://authsu18.alipay.com/login/sendSmsB.json'

        self.rsaPublicKey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmSzXAhW5ktEooSjuZaP0bmE946sR9RVTccHHhQjSbmOpwAO9sRFWiYWAj49vZzzaGa9x7S9aewUdA9AePiOPyIjbzTv60kUJmB5+L85Idd3rx3M7coniHAVPGRWqpItwPj2gbDQlhFxeII6/FZdnOmmo1NHHL/fUebSTNnFbH1QnyU0ri9KYf9fcXREM0ZcWZAW/vZKamjATCEKEq2nimL+4S4JeENnDnipva7ws6m+ApSQHkGV1nnrwfDWmew3MArSTCntGN0bYaZE7sxX8GU9AwPyKagokxQX4GmvEHZfOT2bgMXLk3GJEREFJhRGwRk1D5DQsR1oqCPB0ZLQoVQIDAQAB'
        self.json_token = ''
        self.headers.update(head)

    def __H5_init(self):
        url = 'https://auth.alipay.com/login/h5Login.htm?goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK'
        res = self.get(url,hooks={'response':self.__get_token},headers={'upgrade-insecure-requests':'1'})
        url = 'https://rds.alipay.com/ua_authcenter_h5_login_password.js?&2019080209'
        res = self.get(url,headers={'referer':'https://auth.alipay.com/login/h5Login.htm?goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK'})
        # print(res)
        res = self.alipay_umdata('https://auth.alipay.com/login/h5Login.htm','0000000000000A2126231E1B',headers={'referer':'https://auth.alipay.com/login/h5Login.htm?goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK','origin':'https://auth.alipay.com'})
        umdata_json = res.json()
        self.cookies.set('_umdata',umdata_json.get('id',''),domain='auth.alipay.com',path='/')
        return res

    
    def __sms_init(self):
        url = 'https://authsu18.alipay.com/login/smsLoginB.htm?loginScene=H5_PWD_LOGIN&goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK&mobile=15623143699'

        res = self.get(url,hooks={'response':self.__get_token})
        # print(res)
        with open('./a.txt','w') as f:
            f.write(res.text)


    def __get_token(self,res,*args,**kw):
        # print(res.url)
        json_data = {}
        form_token = []
        try:
            json_data = res.json()
        except JSONDecodeError as _:
            # print(e)
            form_token = re.findall(r'window.form_tk = "(.*?)"',res.text)
        if json_data:
            self.json_token = json_data.get('_json_token','')
        if form_token:
            self.json_token = form_token[0]
        


    def H5_login(self,user_name:str,user_pwd:str):
        self.__H5_init()
        payload = {
            'goto':'https://render.alipay.com/p/f/cjbb/index.html?chInfo=ch_homepage__chsub_yaofeng__zidingyi_quanqiuye&chinfo=ALIPAY_HOME_ROTATION&trace=true&cdpchinfo=ALIPAY_HOME_ROTATION&cdptrace=true&scm=1.cdp.2019010900010100000005408970.1150708207656632320._._._&__webview_options__=bizScenario%3DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320&area=HK',
            'loginScene':'H5_PWD_LOGIN',
            '_input_charset':'utf-8',
            '_output_charset':'utf-8',
            'ctoken':self.cookies.get('ctoken'),
            '_json_token':self.json_token,
            'logonId':user_name,
            'password':self.RSAencrypt(self.rsaPublicKey,user_pwd),
            'json_ua':'092n+qZ9mgNqgJnCG0Zu8+4wrTDv8m+ybHUdNQ=|nOiH84vyhfCL8on8hfOI/l4=|neiHGXz6UeRW5k4rRCGFNFfvXvBB80n4myKKP4kllyZDLEnTf85p22HXshKy|mu6b9JE5kxy1HrEJc95K+EDRV9t8y2TgZcFoEajfcdx1/4c+qs9v|m++T/GIUew59CmUccxaIOUEqQNeyErI=|mOOM6Yws|meWK74oq|luKW+WcCqR6pGqzRo9F1zXrRZ9+r0KEFqga1Ea3cesh4CqUXvRGg0mTUYu1f9VnobRy3ALAynS+FKZgOqACxGZkSashbwUbka/lz/24HrR+oGpoxhjGCNFwpUSejy77GszpSJ18qoxa+D6gAtcRgz2PQdMi5H60ddQB4DYQ3XypSJ64HbxpiF544lTCV/YjwhQygEbYepdR/yHjXv8qyxE3rQMx91GYOewN18lT/XfZE9FzvS+FJ60nvRPJK703xVedO5lf9X/1A7EvnVvxA7E76QuZX40/3S+OL/obziiyHK5ozgemc5JIVkR6SAYUZuzCiMroYjR+IDJsXhRR8CXEEfcp/233VvciwxkH2Q/tTO042QzqcO4guhSmYMYPrnuaQF5MckAOHG7kyoDC4Go8dig6ZFYcWfgtzBn/Zfs16z2vNZQ14AHbxRvNL44v+hvOKPJoqQjdPOb7Kux26CXgNfgp2BXECfg1+DXkKfg1+DX4Nfg11AnEKdgx/DnoOdgV/DHcCcQtyCnMKfAl/CnkIqtt5CKrCt8+6w2HDedF0zWHJc9Fj0GfLech+3H4WYxtt6k/jXshuxnfTZsp4EGUdaBBm4WXqZvVx7U/EVsZO7HnrfPhv43Hgkeme5p7vm+6b6JvjkuaS6pnjkOue7Zfulu+W4JXjluWN+ID1jCidNZH5jPSCBY4AadlrzmLNZeWR5Z/nlOKW6pzqad1pGL4MvNm207YWtg==|l+GOEGMMfxBnFGcIcgFyHWoZagV/DH8QZxRnCHIBctJy|lOyDHXj1V+dV8FzzWz5Rz7rPtNuu2qYGaRp1EHUabxxlH78f|le+AHnv2VORW81/wWD1SJkk8TzVD40M=|kuiHGXzxU+NR9Fj3XzpVJkk+RzRH50c=|k+mGGH3wUuJQ9Vn2XjtUIE83QTVJ6Uk=|kOiHGXzxU+NR9Fj3XzpVy77Ks9yp3KQEaxh3EncYYBdgE7MT|keiHGXzxU+NR9Fj3XzpVIl4xQi1ULlsuji4=|jveYBmPuTPxO60foQCVKMkQrWDdNPk01lTU=|j/aZB2LvTf1P6kbpQSRLM0QrWDdNOEA0lDQ=|jPWaBGHsTv5M6UXqQidIMEMsXzBKPUg9nT0=|jfSbBWDtT/9N6ETrQyZJMUUqWTZMNk87mzs=|ivOcAmfqSPhK70PsRCFOOUUqWTZMMEs3lzc=|i/KdA2brSflL7kLtRSBPN0ItXjFKP0wwkDA=|iPGeAGXoSvpI7UHuRiNMNEAvXDNPPEswkDA=|ifCfAWTpS/tJ7EDvRyJNNUItXjFNO08zkzM=|hv+QDmvmRPRG40/gSC1COkAvXDNHNEc9S+tL|h/6RD2rnRfVH4k7hSSxDO0EuXTJGMks3S+tL|hPOA85zvgPWa7pntgvSM9pnhnfKI8J/rn+iH85zokf6I9JvtlvmP9Zrum/SB9JvumvWA85zolPuP9JvvlfqO95jslPuP+JfjlfqO+1s='
        }
        res = self.post(self.login_url,data=payload,headers={'referer':'https://auth.alipay.com/login/h5Login.htm?goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK','x-csrf-token':self.cookies.get('ctoken'),'origin':'https://auth.alipay.com','x-requested-with':'XMLHttpRequest'},hooks={'response':self.__get_token})
        return res
    
    def AlipaySMStoken(self,phone:'手机号'):
        self.__sms_init()
        payload = {
            'mobile':phone,
            'areaCode':86,
            'loginScene':'H5_PWD_LOGIN',
            'goto':'https://render.alipay.com/p/f/cjbb/index.html?chInfo=ch_homepage__chsub_yaofeng__zidingyi_quanqiuye&chinfo=ALIPAY_HOME_ROTATION&trace=true&cdpchinfo=ALIPAY_HOME_ROTATION&cdptrace=true&scm=1.cdp.2019010900010100000005408970.1150708207656632320._._._&__webview_options__=bizScenario%3DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320&area=HK',
            '_input_charset':'utf-8',
            '_output_charset':'utf-8',
            '_json_token':self.json_token,
            'json_ua':'092n+qZ9mgNqgJnCG0Zu8+4wrTDv8m+ybHUdNQ=|nOiH84vyhfCL8on8hfOI/l4=|neiHGXz6UeRW5k4rRCGFNFfvXvBB80n4myKKP4kllyZDLEnTf85p22HXshKy|mu6b9JE5kxy1HrEJc95K+EDRV9t8y2TgZcFoEajfcdx1/4c+qs9v|m++T/GIUew59CmUccxaIOUEqQNeyErI=|mOOM6Yws|meWK74oq|luKW+WcCqR6pGqzRo9F1zXrRZ9+r0KEFqga1Ea3cesh4CqUXvRGg0mTUYu1f9VnobRy3ALAynS+FKZgOqACxGZkSashbwUbka/lz/24HrR+oGpoxhjGCNFwpUSejy77GszpSJ18qoxa+D6gAtcRgz2PQdMi5H60ddQB4DYQ3XypSJ64HbxpiF544lTCV/YjwhQygEbYepdR/yHjXv8qyxE3rQMx91GYOewN18lT/XfZE9FzvS+FJ60nvRPJK703xVedO5lf9X/1A7EvnVvxA7E76QuZX40/3S+OL/obziiyHK5ozgemc5JIVkR6SAYUZuzCiMroYjR+IDJsXhRR8CXEEfcp/233VvciwxkH2Q/tTO042QzqcO4guhSmYMYPrnuaQF5MckAOHG7kyoDC4Go8dig6ZFYcWfgtzBn/Zfs16z2vNZQ14AHbxRvNL44v+hvOKPJoqQjdPOb7Kux26CXgNfgp2BXECfg1+DXkKfg1+DX4Nfg11AnEKdgx/DnoOdgV/DHcCcQtyCnMKfAl/CnkIqtt5CKrCt8+6w2HDedF0zWHJc9Fj0GfLech+3H4WYxtt6k/jXshuxnfTZsp4EGUdaBBm4WXqZvVx7U/EVsZO7HnrfPhv43Hgkeme5p7vm+6b6JvjkuaS6pnjkOue7Zfulu+W4JXjluWN+ID1jCidNZH5jPSCBY4AadlrzmLNZeWR5Z/nlOKW6pzqad1pGL4MvNm207YWtg==|l+GOEGMMfxBnFGcIcgFyHWoZagV/DH8QZxRnCHIBctJy|lOyDHXj1V+dV8FzzWz5Rz7rPtNuu2qYGaRp1EHUabxxlH78f|le+AHnv2VORW81/wWD1SJkk8TzVD40M=|kuiHGXzxU+NR9Fj3XzpVJkk+RzRH50c=|k+mGGH3wUuJQ9Vn2XjtUIE83QTVJ6Uk=|kOiHGXzxU+NR9Fj3XzpVy77Ks9yp3KQEaxh3EncYYBdgE7MT|keiHGXzxU+NR9Fj3XzpVIl4xQi1ULlsuji4=|jveYBmPuTPxO60foQCVKMkQrWDdNPk01lTU=|j/aZB2LvTf1P6kbpQSRLM0QrWDdNOEA0lDQ=|jPWaBGHsTv5M6UXqQidIMEMsXzBKPUg9nT0=|jfSbBWDtT/9N6ETrQyZJMUUqWTZMNk87mzs=|ivOcAmfqSPhK70PsRCFOOUUqWTZMMEs3lzc=|i/KdA2brSflL7kLtRSBPN0ItXjFKP0wwkDA=|iPGeAGXoSvpI7UHuRiNMNEAvXDNPPEswkDA=|ifCfAWTpS/tJ7EDvRyJNNUItXjFNO08zkzM=|hv+QDmvmRPRG40/gSC1COkAvXDNHNEc9S+tL|h/6RD2rnRfVH4k7hSSxDO0EuXTJGMks3S+tL|hPOA85zvgPWa7pntgvSM9pnhnfKI8J/rn+iH85zokf6I9JvtlvmP9Zrum/SB9JvumvWA85zolPuP9JvvlfqO95jslPuP+JfjlfqO+1s='
        }
        res = self.post(self.smsToken_url,data=payload,headers={'referer':'https://authsu18.alipay.com/login/smsLoginB.htm?loginScene=H5_PWD_LOGIN&goto=https%3A%2F%2Frender.alipay.com%2Fp%2Ff%2Fcjbb%2Findex.html%3FchInfo%3Dch_homepage__chsub_yaofeng__zidingyi_quanqiuye%26chinfo%3DALIPAY_HOME_ROTATION%26trace%3Dtrue%26cdpchinfo%3DALIPAY_HOME_ROTATION%26cdptrace%3Dtrue%26scm%3D1.cdp.2019010900010100000005408970.1150708207656632320._._._%26__webview_options__%3DbizScenario%253DALIPAY_HOME_ROTATION.5455.122005.1150708207656632320%26area%3DHK&mobile=15623143699','x-csrf-token':self.cookies.get('ctoken'),'x-requested-with':'XMLHttpRequest'},hooks={'response':self.__get_token})
        return res
    

if __name__ == '__main__':
    ts = Alipay()
    # res = ts.hex2Base64('8a8b918209bfc6bd88674d6da638094f7d15a024cb627c7598f73459da230c3559cdfa88192470cdc1a09fb99697ebb8d52ff3455f6b8fb82676db8533f103122649c6a1651501f509b41f5b1c24cbb0d109edfb3d1f41cdea30e072282c7c7f248d3a9b7ca90eb0d7a96fa9420a3e9faaaec199b5ae1196ad1332f6d3b2bd392f34c6c20b85805258182755e26fa7c6a42385eea2cbffd901e9b9d96b72b59f276cb947388166a976d27e4d59eabd4d37ec44d36ef54b042a3ae5eec177cde71477650294aa0833b7e62568a21db8a2e846647d3b3d3450c887a5beb0b88d28ac58658f74dd87c20494464bdf7b601bd7c24ccd923d185640560935727bc46a')
    # res = ts.str2key(ts.rsaPublicKey)
    # res = ts.AlipaySMStoken('')
    res = ts.H5_login('1347774798','1234567')
    # pubkey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmSzXAhW5ktEooSjuZaP0bmE946sR9RVTccHHhQjSbmOpwAO9sRFWiYWAj49vZzzaGa9x7S9aewUdA9AePiOPyIjbzTv60kUJmB5+L85Idd3rx3M7coniHAVPGRWqpItwPj2gbDQlhFxeII6/FZdnOmmo1NHHL/fUebSTNnFbH1QnyU0ri9KYf9fcXREM0ZcWZAW/vZKamjATCEKEq2nimL+4S4JeENnDnipva7ws6m+ApSQHkGV1nnrwfDWmew3MArSTCntGN0bYaZE7sxX8GU9AwPyKagokxQX4GmvEHZfOT2bgMXLk3GJEREFJhRGwRk1D5DQsR1oqCPB0ZLQoVQIDAQAB'
    # res = ts.RSAencrypt(pubkey,'1234567')
    print(res.text)