# coding:utf-8


from types import FunctionType,LambdaType,CodeType


class ParamsNotFound(Exception):

    def __init__(self):
        pass


'''各个日志的区别应该是日志格式的区别，那么需要有一个总的日志类来实现接受不同的格式来实现不同的应用'''



class ParamsLog(object):
    '''参数日志装饰器
    这个需要继承一个日志类来自动实现日志的数据配置，
    而它本身只需要设定自身的日志格式

    需要记录参数传递日志的类继承此类，然后此类将会记录参数的传递以及数据的导出
    使用的是getattribute方法，拦截所有请求调用，只需要判断返回的数据类型是不是函数即可
    如果是函数那么使用装饰器装饰此函数，然后在装饰器函数中得到参数以及相应记录到日志
    '''
    def __init__(self):
        pass
    
    def __getattribute__(self,name):
        val = object.__getattribute__(self,name)
        if isinstance(val,(FunctionType,LambdaType)):
            return self(val)
        else:
            return val
    
    def __call__(self):
        pass

class ApiLog(object):

    def __init__(self):
        pass
    
    def __call__(self):
        pass


