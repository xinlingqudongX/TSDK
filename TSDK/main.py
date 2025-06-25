from api.taobao.h5 import TaobaoH5
from api.taobao.open import TaobaoOpen
from api.douyin.h5 import DouyinH5
from api.eleme.h5 import ElemeH5
import json



if __name__ == '__main__':
    # h5 = TaobaoH5()
    # h5.urlCreateFunc('https://h5api.m.taobao.com/h5/mtop.taobao.shop.impression.logo.get/1.0/?jsv=2.6.1&appKey=12574478&t=1702987766953&sign=206ee688cc2fea46ff035bccb349579b&api=mtop.taobao.shop.impression.logo.get&v=1.0&type=jsonp&secType=1&preventFallback=true&dataType=jsonp&callback=mtopjsonp5&data=%7B%22sellerId%22%3A%22499878111%22%2C%22shopId%22%3A%2262643782%22%7D')
    # h5 = DouyinH5()
    h5 = ElemeH5()
    # h5.urlCreateFunc('https://waimai-guide.ele.me/h5/mtop.alsc.user.session.ele.check/1.0/?jsv=2.7.5&appKey=12574478&t=1750813282236&sign=b11f35a93b31d469eaaf13223ff3f692&api=mtop.alsc.user.session.ele.check&v=1.0&type=originaljson&dataType=json&timeout=5000&mainDomain=ele.me&subDomain=waimai-guide&pageDomain=ele.me&H5Request=true&syncCookieMode=true')
    res = h5.MtopAlscUserSessionEleCheck()
    if res:
        print(res)