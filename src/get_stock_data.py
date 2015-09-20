#encoding: gb2312
'''
@author: john
'''
import requests #使用web接口的类库
import json #解析返回的json格式
import re #格式化不正规的json字符串
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
def parse_daily_data(raw_data):
    daily_data = {}
    daily_data['name'] = raw_data[0:raw_data.find('=')]
    daily_data['data_field'] = 'date open close high low vol'
    daily_data['data'] = raw_data[raw_data.find('=')+2:-2].split('\\n\\\n')    
    daily_data['data'].pop(0) #remove the first and the last empty item
    daily_data['data'].pop()
    #日期        开盘        收盘        最高        最低        成交量(万)
    #100104 3289.75 3243.76 3295.28 3243.32 109447927    
    return daily_data
        
if __name__ == '__main__':

#     url = 'https://jy.yongjinbao.com.cn/winner_gj/gjzq/exchange.action'
#     params = {
#         'CSRF_Token': 'undefined',
#         'timestamp': '0.602064706152305',
#         'request_id': 'mystock_405'
#     }    
#     raw_data = requests.session.get(url, params=params).content    
    
    for year in xrange(10, 16):
        url = 'http://data.gtimg.cn/flashdata/hushen/daily/%02d/sh000001.js'%(year)
        raw_data = requests.get(url).content
        parsed_data = parse_daily_data(raw_data)
        pass
    
