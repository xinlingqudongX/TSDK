# TSDK
淘宝爬虫SDK，用于淘宝开放平台或淘宝登录爬取


##  淘宝系列爬虫系列SDK
  
  - SDK更新到第二版，对一部分进行了优化
    * 优化掉通用类，此类本身最开始是为了能够使用无授权API，但是之后发现臃肿繁杂，还不如直接请求网址URL，觉得有些画蛇添足了，所以直接去掉
    * 优化开放平台类，繁杂的配置文件，多余的加载，我用了Node的SDK之后发现还不如Node的方便，只需要传入API名称和数据就行了，那么我弄了配置文件又有什么用，没有达到简单可用的目的遂改成Node一样的方式请求数据
    * 优化H5API类，经过我思考后觉得配置文件太过繁杂，且不够灵活也不多变，爬虫本身就是需要多变的，所以移除配置文件，通过传递参数直接构建，更加灵活方便

  - 还有部分功能未实现，例如日志功能和请求重放功能，以及新添加的网站

```python
  from TSDK.mTop import Client

  top = Client()
  #获取淘宝二维码，可以通过扫码登录淘宝
  umid_token = top.getUmidToken()
  res = top.login(umid_token)
  # 返回了淘宝登录的二维码
  print(res.text)
  data = json.loads(res.text)
  thr = top.checkState(data['lgToken'],umid_token,30)
  thr.start()
  
  #手机号登录淘宝
  phone = input('请输入手机号：')
  smsdata = top.sendMsg(phone)
  if smsdata.get('success'):
    smscode = input('请输入验证码：')
    res = top.msgForm(phone,smscode,{'smsTime':smsdata.get('smsTime'),'smsToken':smsdata.get('smsToken')})
    # print(res.text)
  else:
    print(smsdata.get('message'))

  #设置开放平台的appkey和密钥，然后传递API和配置可以直接获取数据
  top.open.config['appkey'] = ''
  top.open.config['appsecret'] = ''

  # 使用淘宝开放平台的API获取数据
  res = top.open.execute('taobao.tbk.item.get',{
        'fields':'num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick',
        'q':'女装',
        'cat':'16,18'
    })
  print(res.text)

  #通过淘宝的H5API获取宝贝详情
  res = top.H5.execute({
        'api':'mtop.taobao.detail.getdetail',
        'v':'6.0',
        'jsv':'2.4.8',
        'dataType':'json',
        'type':'json',
        'ttid':'2017%40taobao_h5_6.6.0',
        'AntiCreep':'true',
        'data':{
            'itemNumId':'585559878166'
        }
    })
  print(res.text)
```



```python
  #API请求日志的记录,SDK对象继承自requests的Session类，可以通过添加hook来获取响应
  #请参考requests高级用法：http://docs.python-requests.org/zh_CN/latest/user/advanced.html
  def console(res):
    print(res.url)
    print(res.text)

  top.H5.hooks['response'] = [console]

```

### Cookie的同步

```python
  from requests.cookies import RequestsCookieJar

  dt = top.H5.cookies.get_dict('.login.taobao.com')

  jar = RequestsCookieJar()
  for name in dt:
    jar.set(name,dt[name],path='/',domain='.login.taobao.com')
  
  # 通过设置cookie来共享登录状态
  top.cookies.update(jar)

```

### 淘宝H5API的使用
  1.  在浏览器中找到请求的接口，例如：https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=1535803615228&sign=fa7b5f3312f9727a25662162bf502aff&api=mtop.taobao.detail.getdetail&v=6.0&dataType=json&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=json&data=%7B%22itemNumId%22%3A%224362046464%22%7D
  这是请求商品详情的接口

  2.  将链接中的参数提取然后传入请求中

###  淘宝APP端API

  学了一段时间的Hook，逆向，结果看来APP端的加密是破解不出来了。。。。，就分享一下找到的API吧


### 淘宝短信登录

  测试了淘宝短信登录，请求中需要一个ua参数，这个参数是算法生成出来的，经过测试应该是根据平台登录的浏览器环境记录下来，所以如果ua参数不对的话那么就登录不了，会出现滑动验证
  如果要进行短信登录测试的话，替换ua参数为你自己浏览器上面的ua参数，在源码中修改
  
