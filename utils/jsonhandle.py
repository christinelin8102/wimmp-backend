import json
from argparse import Namespace
from flask import jsonify
import datetime
import json
import json
import numpy as np

list_ignorewords = ['metadata','query']


def clearTheNull(dic,clearList):
    # delList = []
    # for k,v in dic.items():
    #     if (v == ''):
    #         delList.append(k)
    # for k in delList:
    #     dic[k] = -1
    for k in clearList:
        if k in dic and dic[k] == '':
            dic[k] = -1
    return dic

def getJsonData(data):
    if isinstance(data,list) != True:
        return json.dumps(dictModel(data),cls = MyJsonEncoder)
    else:
        res = '['
        start = 0
        for x in data:
            if start != 0:
                res = res + ','
            #strp = jsonify(x.__dict__)
            txt = dictModel(x)
            print(txt)
            strp = json.dumps(txt,cls = MyJsonEncoder) 
            res = res + strp
            start = start + 1
        res = res + ']'
        return res
       
def dictModel(inst):

    return dict((name, getattr(inst, name)) for name in dir(inst)   
       if not name.startswith('_')  and not callable(getattr(inst, name))
           and not name in list_ignorewords)   
        
def transferVOtoEO(vo,eo,ignoreList = []):
    for key, value in vo.items():   
        if key in ignoreList:
            print(key)
            continue       
        setattr(eo, key, value)
    return eo

def transferEOtoVO(eo,vo,pidname):
    for name in dir(eo):
        if not name.startswith('_')  and not callable(getattr(eo, name)) \
           and not name in list_ignorewords:
           if name == pidname:
               setattr(vo,"id",getattr(eo,name))
           else:
               setattr(vo,name,getattr(eo,name))
    return vo              

def dumpSimpleObject(obj):
    return json.dumps(dictModel(obj))


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(json.JSONEncoder,obj)

    # list 转成Json格式数据
def listToJson(lst):
        keys = [str(x) for x in np.arange(len(lst))]
        list_json = dict(zip(keys, lst))
        str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
        return str_json


