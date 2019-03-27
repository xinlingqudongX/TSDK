# coding:utf-8


from types import FunctionType,LambdaType,CodeType
from functools import wraps



class Tool(object):
    '''
        准备使用装饰器控制请求的重放，但是还是没想好由外部控制还是内部设定
    '''
    def __init__(self,func):
        wraps(func)(self)
        self.ncalls = 0
    
    def __call__(self,*args,**kw):
        self.ncalls += 1
        return self.__wrapped__(*args,**kw)
    
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self,instance)


class Logs(object):
    pass

class Retry(object):

    def __init__(self,log:bool=False,format:str='',callback:FunctionType=None):
        self.log = log
        self.format = format
        self.callback = callback
    
    def __call__(self,func,*args,**kw):

        print('call:')
        @wraps(func)
        def wrapper(obj,**kw):
            res = func(obj,**kw)
            print('Ending')
            res = self.callback(res,obj) if self.callback else res
            return res
        return wrapper

@Retry()
def execute(**kw):
    print(kw)
    return kw

class G:
    @Retry()
    def execute(self,**kw):
        return kw




if __name__ == '__main__':
    res = G().execute(a=3,b=4,c=5)
    print(res)





