# coding:utf-8

import sys
sys.path.append('.')

from taobao.淘宝H5 import TB_H5
from taobao.淘宝开放平台 import TB_openPlatform
from taobao.SDK基类 import Base

import json
from threading import Thread
from time import sleep


class Client(Base):

    def __init__(self):
        super(Client,self).__init__()
        self.H5 = TB_H5()
        self.open = TB_openPlatform()
    

    def login(self,timeout:int=30,domain:str='www.taobao.com'):
        self.defaulturl = domain
        self.get(f'https://login.taobao.com/member/login.jhtml?redirectURL={domain}')
        umid_token = self.getUmidToken()
        res = self.get(f'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=tb&appkey=00000000&umid_token={umid_token}')
        data = json.loads(res.text)
        thd = self.checkState(data['lgToken'],umid_token,timeout)
        return res
    
    def checkState(self,lgToken,umid_token,*args):
        '''闭包中访问不到函数的局域变量，也是不知道怎么回事'''
        def run():
            # print(args)
            timeout = args[0]
            locals()['lgToken'] = lgToken
            locals()['umid_token'] = umid_token
            locals()['timeout'] = timeout
            # print(lgToken)
            while timeout > 0:
                res = self.get(f'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken={lgToken}&defaulturl={self.defaulturl}')
                data = json.loads(res.text)
                if data['code'] == '10006':
                    url = data['url'] + '&umid_token=' + umid_token
                    self.get(url)
                    print('扫码成功')
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
        thd.start()
        return thd





if __name__ == '__main__':
    
    top = Client()
    res = top.login(30)
    print(res.text)