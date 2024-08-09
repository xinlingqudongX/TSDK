

#### msToken的获取
- 经过测试，是通过POST请求https://mssdk.bytedance.com/web/common来获取的
- 当初次没有msToken的时候，传递的query string参数并没有msToken
- 最主要的参数在于payload中
![alt text](strData_payload.png)

- strData参数包含有加密的参数，当msToken更换的时候，旧的msToken还可以使用