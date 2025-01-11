from TSDK.api.douyin.h5 import DouyinH5
from TSDK.api.taobao.h5 import TaobaoH5
import pytest

def df(x):
    return x + 1


def test_func():
    assert df(3) == 4

def bb_func():
    assert df(3) == 4

def test_create_types():
    '''测试创建数据类型'''
    client = TaobaoH5()
    client.debug = True
    client.createTypes('LoginFormData', {"appName":"taobao","appEntrance":"taobao_pc","_csrf_token":"Uom9976TSI0WXXUPzQKgO","umidToken":"229a0385e86f7247b2e58f525a41e845ed23a149","hsiz":"124e06e9e0fb161d484465b80808e9be","newMini2":"true","bizParams":"taobaoBizLoginFrom=taobao-home","full_redirect":"false","mainPage":False,"style":"mini","appkey":"00000000","from":"sm","isMobile":False,"lang":"zh_CN","returnUrl":"https://www.taobao.com/","fromSite":0})

    pass

def test_check_login():
    '''测试扫码登录'''
    client = TaobaoH5()
    client.debug = True
    client.verify = False

    login = client.qrLogin()
    
    assert login == True

    data = client.getUserSimple()
    print(data)