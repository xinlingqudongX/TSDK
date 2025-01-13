from typing import Generic, TypedDict, Union, List, Dict, Any, Optional, TypeVar
from enum import Enum

T = TypeVar('T')

class QrGenerateData(TypedDict):
    t: int
    codeContent: str
    ck: str
    resultCode: int
    processFinished: bool

class QrGenerateContent(Generic[T], TypedDict):
    data: T
    status: int
    success: bool

class QrLoginRes(TypedDict):
    content: QrGenerateContent[QrGenerateData]
    hasError: bool

class QrStateRes(TypedDict):
    message: str
    success: bool
    code: str
    url: str

class SendSmsData(TypedDict):
    emailToken: str
    resultCode: int
    smsToken: str

class LoginSmsData(TypedDict):
    resultCode: int
    titleMsg: Optional[str]
    redirect: Optional[bool]
    loginResult: Optional[str]
    loginSucResultAction: Optional[str]
    redirectUrl: Optional[str]
    loginType: Optional[str]
    returnUrl: Optional[str]

class LoginRes(Generic[T], TypedDict):
    content: QrGenerateContent[T]
    hasError: bool

SendSmsRes = LoginRes[SendSmsData]
LoginSmsRes = LoginRes[LoginSmsData]
# {
# 	"content": {
# 		"data": {
# 			"qrCodeStatus": "CONFIRMED",
# 			"asyncUrls": ["https://pass.tmall.hk/add?lid=%E8%8B%B1%E9%9B%84%E4%BA%A6%E6%9E%89%E7%84%B6&_l_g_=Ug%3D%3D&cookie1=Vv6fxNwYboXOnA3gl0xkAY1IBt4Q2MMC3HqyTw83URo%3D&cookie2=1647b2631c394553eb2a7574fc7d3936&cancelledSubSites=empty&sg=%E7%84%B630&_tb_token_=e78eb91113e65&wk_unb=UoH2iZs9kSfwKw%3D%3D&dnk=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&uc1=existShop=false;cookie21=U%2BGCWk%2F7owY3j65jYmjW9Q%3D%3D;cookie15=VFC%2FuZ9ayeYq2g%3D%3D;cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D;pas=0;cookie14=UoYdWxBFA2p5xQ%3D%3D&tracknick=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&unb=1090955643&wk_cookie2=1f948ff13f174c0ca49cd4c823f1d2e2&cookie17=UoH2iZs9kSfwKw%3D%3D&_nk_=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&sgcookie=E100Un7i5fGr6xAulElTnyhLbVSQTrSsDHzgSvy2JPwBK1%2Bcf5XXR8iLWPSJ6btG%2BxoPieBpldeg1do5BmPuS4rvOtl3Cqm0dfaImJNoO29%2BcKg%3D&t=1ec2d722d74091bece6d6cad248db2a1&csg=3f867203&login=true&tmsc=1736606028478000&opi=211.161.187.113&pacc=_au-p0hoACkxoAGolaF-mw==&target=https%3A%2F%2Flist.tmall.hk%2Fsearch_product.htm", "https://pass.fliggy.com/add?lid=%E8%8B%B1%E9%9B%84%E4%BA%A6%E6%9E%89%E7%84%B6&_l_g_=Ug%3D%3D&cookie1=Vv6fxNwYboXOnA3gl0xkAY1IBt4Q2MMC3HqyTw83URo%3D&cookie2=1647b2631c394553eb2a7574fc7d3936&cancelledSubSites=empty&sg=%E7%84%B630&_tb_token_=e78eb91113e65&wk_unb=UoH2iZs9kSfwKw%3D%3D&dnk=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&uc1=existShop=false;cookie21=U%2BGCWk%2F7owY3j65jYmjW9Q%3D%3D;cookie15=VFC%2FuZ9ayeYq2g%3D%3D;cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D;pas=0;cookie14=UoYdWxBFA2p5xQ%3D%3D&tracknick=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&unb=1090955643&wk_cookie2=1f948ff13f174c0ca49cd4c823f1d2e2&cookie17=UoH2iZs9kSfwKw%3D%3D&_nk_=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&sgcookie=E100Un7i5fGr6xAulElTnyhLbVSQTrSsDHzgSvy2JPwBK1%2Bcf5XXR8iLWPSJ6btG%2BxoPieBpldeg1do5BmPuS4rvOtl3Cqm0dfaImJNoO29%2BcKg%3D&t=1ec2d722d74091bece6d6cad248db2a1&csg=3f867203&login=true&tmsc=1736606028478000&opi=211.161.187.113&pacc=_au-p0hoACkxoAGolaF-mw==&target=https%3A%2F%2Fwww.fliggy.com", "https://pass.tmall.com/add?lid=%E8%8B%B1%E9%9B%84%E4%BA%A6%E6%9E%89%E7%84%B6&_l_g_=Ug%3D%3D&lgc=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&cookie1=Vv6fxNwYboXOnA3gl0xkAY1IBt4Q2MMC3HqyTw83URo%3D&cookie2=1647b2631c394553eb2a7574fc7d3936&cancelledSubSites=empty&sg=%E7%84%B630&_tb_token_=e78eb91113e65&wk_unb=UoH2iZs9kSfwKw%3D%3D&dnk=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&uc1=existShop=false;cookie21=U%2BGCWk%2F7owY3j65jYmjW9Q%3D%3D;cookie15=VFC%2FuZ9ayeYq2g%3D%3D;cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D;pas=0;cookie14=UoYdWxBFA2p5xQ%3D%3D&uc3=lg2=UIHiLt3xD8xYTw%3D%3D;vt3=F8dD37F7kozlzFQTy4c%3D;nk2=sCJAj0Qx6%2FoezQ%3D%3D;id2=UoH2iZs9kSfwKw%3D%3D&tracknick=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&uc4=nk4=0%40strXCZmJJA%2BRBVfP5829%2Bv9KgDHU;id4=0%40UOnpLhsAbrpKodYfPTeNjeONFBwL&unb=1090955643&wk_cookie2=1f948ff13f174c0ca49cd4c823f1d2e2&cookie17=UoH2iZs9kSfwKw%3D%3D&_nk_=%5Cu82F1%5Cu96C4%5Cu4EA6%5Cu6789%5Cu7136&sgcookie=E100Un7i5fGr6xAulElTnyhLbVSQTrSsDHzgSvy2JPwBK1%2Bcf5XXR8iLWPSJ6btG%2BxoPieBpldeg1do5BmPuS4rvOtl3Cqm0dfaImJNoO29%2BcKg%3D&t=1ec2d722d74091bece6d6cad248db2a1&csg=3f867203&login=true&tmsc=1736606028478000&opi=211.161.187.113&pacc=nJNJvMf1OHvtzn_IqMmSwA==&target=https%3A%2F%2Fwww.tmall.com"],
# 			"resultCode": 100,
# 			"iframeRedirect": true,
# 			"iframeRedirectUrl": "https://i.taobao.com/my_taobao.htm?nekot=06LQ29LgzffIuw==1736606028477",
# 			"processFinished": true
# 		},
# 		"status": 0,
# 		"success": true
# 	},
# 	"hasError": false
# }

class QrStatus(Enum):
    扫码中 = 'SCANED'
    已过期 = 'EXPIRED'
    已取消 = 'CANCELED'
    已确认 = 'CONFIRMED'
    未扫码 = 'NEW'
    错误 = 'ERROR'

class QrCheckData(TypedDict):
    '''
    SCANED 100
    EXPIRED 100
    CONFIRMED 100
    '''
    qrCodeStatus: QrStatus
    resultCode: int

    asyncUrls: Optional[List[str]]
    iframeRedirect: Optional[bool]
    iframeRedirectUrl: Optional[str]
    processFinished: Optional[bool]

class QrCheckContent(TypedDict):
    data: QrCheckData
    status: int
    success: bool

class QrCheckRes(TypedDict):
    content: QrCheckContent
    hasError: bool
    
class QrStateCode(Enum):
    扫码成功 = '10006'
    正在扫码 = '10001'
    二维码过期 = '10004'
    跳过 = '10000'

class RecommendRes(TypedDict):
    content: Any
    hasError: bool
class ApiRes(TypedDict):
    api: str
    v: str
    ret: List[str]
    data: Dict[str, Any]

class UserSimpleRes(TypedDict):
    nick: str
    userNumId: str
    displayNick: str

class OpenApiErrorMsg(TypedDict):
    code: int
    msg: str
    sub_msg: str
    request_id: str
class OpenApiRes(TypedDict):
    error_response: OpenApiErrorMsg

class BoolStr(Enum):
    true = "true"
    false = "false"

class ShopInfo(TypedDict):
    tmall: BoolStr
    sellerId: str
    shopId: str
    shopLogo: str
    shopName: str

class ShopImpression(TypedDict):
    bizLogoPicList: List[str]
    fansNum: str
    goldenSeller: BoolStr
    aptitude: str
    changeSubscribe2Follow: BoolStr
    city: str
    licenseUrl: str
    nick: str
    ownerChanged: BoolStr
    personalManager: BoolStr
    sellerId: str
    starts: str
    tmall: BoolStr
    xid: str

class LoginFormData(TypedDict):
    appName: str
    appEntrance: str
    _csrf_token: str
    umidToken: str
    hsiz: str
    newMini2: str
    bizParams: str
    full_redirect: str
    mainPage: bool
    style: str
    appkey: str
    isMobile: bool
    lang: str
    returnUrl: str
    fromSite: int

class LoginViewData(TypedDict):
    appEntrance: str
    appName: str
    awscCdn: str
    baxiaLang: str
    currentTime: str
    disableAutoRedirectToWechatAuth: bool
    enableSmsAudio: bool
    foreign: bool
    isMobile: bool
    lang: str
    loginFormData: LoginFormData
    mobile: bool
    nocaptchaAppKey: str
    officialAccountsSnapshotuser: bool
    returnUrl: str
    showAutioSlipCode: bool
    trySilentHasLogin: bool
    umidEncryptAppName: str
    umidServer: str
    umidServiceLocation: str
    umidToken: str



