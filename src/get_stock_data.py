#encoding: gb2312
'''
@author: john
'''
import requests #使用web接口的类库
import json #解析返回的json格式
import re #格式化不正规的json字符串
import sqlite3
class DBClass(object):
    def __init__(self,DB_SQLITE_NAME='stock.db'):        
        try:
            self.sqlite_conn = sqlite3.connect(DB_SQLITE_NAME)
        except sqlite3.Error,e:
            print "connect to sqlite3 failed", "\n", e.args[0]
        self.sqlite_cursor = self.sqlite_conn.cursor()
        
    def create_table(self, table_name):
        sql_str='''CREATE TABLE %s(
        i_index INTEGER PRIMARY KEY, date TEXT, open REAL, close REAL, high REAL, low REAL, vol REAl
        );'''%(table_name)
        try:
            self.sqlite_cursor.execute(sql_str)
        except sqlite3.Error,e:
            print "create table failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
    
    def insert_record(self, table_name, records):
        sql_str='''INSERT INTO %s(date, open, close, high, low, vol) values (?,?,?,?,?,? );'''%(table_name)
        try:
            self.sqlite_cursor.executemany(sql_str, records)
        except sqlite3.Error,e:
            print "insert records failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
        
    def close_db(self):
        self.sqlite_conn.close()
        
def parse_daily_data(raw_data):
    daily_data = {}
    daily_data['name'] = raw_data[0:raw_data.find('=')]
    daily_data['data_field'] = 'date open close high low vol'
    all_data_str = raw_data[raw_data.find('=')+2:-2].split('\\n\\\n')
    all_data_str.pop(0) #remove the first and the last empty item
    all_data_str.pop()    
    all_data = []
    for i in xrange(len(all_data_str)):
        str_temp = all_data_str[i].split()
        data_item = (str_temp[0], float(str_temp[1]), float(str_temp[2]), 
                     float(str_temp[3]), float(str_temp[4]), float(str_temp[4]))
        all_data.append(data_item)
    daily_data['data'] = all_data
    #日期        开盘        收盘        最高        最低        成交量(万)
    #100104 3289.75 3243.76 3295.28 3243.32 109447927    
    return daily_data

def get_stock_data(db, stock_name, year_range):    
    db.create_table(stock_name)
    for year in xrange(year_range[0], year_range[1]+1):
        url = 'http://data.gtimg.cn/flashdata/hushen/daily/%02d/%s.js'%(year, stock_name)
        raw_data = requests.get(url).content
        if raw_data.find('404 Not Found') != -1:
            print 'Year %02d, stock %s, no data'%(year, stock_name)
            continue        
        parsed_data = parse_daily_data(raw_data)
        db.insert_record(stock_name, parsed_data['data'])
    
if __name__ == '__main__':

#     url = 'https://jy.yongjinbao.com.cn/winner_gj/gjzq/exchange.action'
#     params = {
#         'CSRF_Token': 'undefined',
#         'timestamp': '0.602064706152305',
#         'request_id': 'mystock_405'
#     }    
#     raw_data = requests.session.get(url, params=params).content
    db = DBClass('stock.db')      
    stock_name_list = ['sh000001', 'sz399001', 'sh000300']
    for stock_name in stock_name_list:
        get_stock_data(db, stock_name, (90,99))
        get_stock_data(db, stock_name, (00,15))
    db.close_db()
    