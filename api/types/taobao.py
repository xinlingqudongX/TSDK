from typing import TypedDict, Union, List, Dict, Any
from enum import Enum


class QrLoginRes(TypedDict):
    adToken: str
    success: bool
    lgToken: str
    message: str
    url: str

class QrStateRes(TypedDict):
    message: str
    success: bool
    code: str
    url: str

class QrStateRes2Data(TypedDict):
    ck: str
    codeContent: str
    resultCode: int
    t: int
    
class QrStateCode(Enum):
    扫码成功 = '10006'
    正在扫码 = '10001'
    二维码过期 = '10004'
    跳过 = '10000'

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