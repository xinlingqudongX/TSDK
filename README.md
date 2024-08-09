# TSDK
淘宝爬虫SDK，用于淘宝开放平台或淘宝登录爬取


##  淘宝系列爬虫系列SDK
  
  - 第三版

```python
from TSDK.api.taobao.h5 import TaobaoH5

client = TaobaoH5()
# 触发登录显示二维码，扫码后即可登录
loginStatus = client.qrLogin()
if not loginStatus:
    print('登录失败')
```

### 淘宝H5API的使用
  1.  在浏览器中找到请求的接口，例如：https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=1535803615228&sign=fa7b5f3312f9727a25662162bf502aff&api=mtop.taobao.detail.getdetail&v=6.0&dataType=json&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=json&data=%7B%22itemNumId%22%3A%224362046464%22%7D
  这是请求商品详情的接口

  2.  将链接中的参数提取然后传入请求中
  
