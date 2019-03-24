# coding:utf-8


from __future__ import absolute_import


try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base

from time import time
import json

class JD(Base):

    def __init__(self):
        super(JD,self).__init__()
    

    def login(self):
        t = int(time()*1000)
        url = f'https://qr.m.jd.com/show?appid=133&size=147&t={t}'
        img = self.get(url).content
        th = self.checkState()
        return img
    
    def checkState(self,cookieName:str='wlfstk_smdl',timeout=30):
        token = self.cookies.get(cookieName)
        def run():
            nonlocal timeout
            while timeout > 0:
                res = self.get('https://qr.m.jd.com/check?appid=133&token={token}')
                data = json.loads(res.text)
                if data['code'] == 200:
                    ticket = data['ticket']
                    res = self.get(f'https://passport.jd.com/uc/qrCodeTicketValidation?t={ticket}')
                    data = json.loads(res.text)
                    if not data['returnCode']:
                        self.get(data['url'])
                    break
                else:
                    print(data['msg'])
            



if __name__ == '__main__':
    pass