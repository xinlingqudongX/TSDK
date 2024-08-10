from api.taobao.h5 import TaobaoH5
from api.taobao.open import TaobaoOpen
from api.douyin.h5 import DouyinH5
import json



if __name__ == '__main__':
    # h5 = TaobaoH5()
    # h5.urlCreateFunc('https://h5api.m.taobao.com/h5/mtop.taobao.shop.impression.logo.get/1.0/?jsv=2.6.1&appKey=12574478&t=1702987766953&sign=206ee688cc2fea46ff035bccb349579b&api=mtop.taobao.shop.impression.logo.get&v=1.0&type=jsonp&secType=1&preventFallback=true&dataType=jsonp&callback=mtopjsonp5&data=%7B%22sellerId%22%3A%22499878111%22%2C%22shopId%22%3A%2262643782%22%7D')
    h5 = DouyinH5()