# coding:utf-8

#   此文件目的是能够控制文件的输出和加载


import os
from pathlib import Path
import json
import datetime
from collections import OrderedDict



class FileSystem(object):

    def __init__(self,file_path='./Api.json'):
        self.file_path = file_path
        self.reload()
    

    def reload(self):
        with open(Path(self.file_path).absolute(),encoding='utf-8') as f:
            self.Api = json.load(f,object_pairs_hook=OrderedDict)
    
    def getjson(self,name:str=""):
        return self.Api.get(name) if name else self.Api
    
