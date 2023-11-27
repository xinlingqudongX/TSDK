from api.taobao.h5 import TaobaoH5
from api.taobao.open import TaobaoOpen
from api.eleme.h5 import ElemeH5



if __name__ == '__main__':
    h5 = ElemeH5()
    h5.urlCreateFunc('https://waimai-guide.ele.me/h5/mtop.alsc.wamai.store.detail.business.tab.phone/1.0/5.0/?jsv=2.7.2&appKey=12574478&t=1701088333698&sign=630d4b8b2f0a555bb22462fb62b990be&api=mtop.alsc.wamai.store.detail.business.tab.phone&v=1.0&type=originaljson&dataType=json&timeout=10000&mainDomain=ele.me&subDomain=waimai-guide&H5Request=true&ttid=h5%40chrome_pc_119.0.0.0&SV=5.0&bx_et=dBlwr-v97CdZ1VE6eRV4ao-HpLVTs7KWmjZboq005lqiGPDFgDnznRTTsJ03urr0mR2G-64zyPq0jPmEomi-C1NMWE54A4YT1FF1irqIb-GXWsiFgDnzIsGqkszmomLTcFpIWVFYi3t7gQgtWkGeV36by_Z7MSxWVmE0B6Vx4jNrWGh4FNXFT-xoykcnKB6MDaqYYsfPyPyMlV6fZ_X0SREuRkWZyiUhvhlxQiX4IyUUVe8UdPQ83', method='POST', formdata={"eleStoreId":"E6480404258831972301"})
    h5.MtopAlscWamaiStoreDetailBusinessTabPhone({
        'eleStoreId': 'E6480404258831972311'
    })