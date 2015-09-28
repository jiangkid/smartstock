#encoding: utf-8
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
        
    def create_stock_daily_table(self, table_name):
        sql_str='''CREATE TABLE IF NOT EXISTS %s(
        i_index INTEGER PRIMARY KEY, date TEXT UNIQUE, open REAL, close REAL, high REAL, low REAL, vol REAl
        );'''%(table_name)
        try:
            self.sqlite_cursor.execute(sql_str)
        except sqlite3.Error,e:
            print "create table failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
    
    def insert_stock_daily_record(self, table_name, records):
        sql_str='''INSERT OR IGNORE INTO %s(date, open, close, high, low, vol) values (?,?,?,?,?,? );'''%(table_name)
        try:
            self.sqlite_cursor.executemany(sql_str, records)
        except sqlite3.Error,e:
            print "insert records failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
        
    def create_stock_sub_table(self, table_name):
        sql_str='''CREATE TABLE IF NOT EXISTS %s(
        i_index INTEGER PRIMARY KEY, date TEXT UNIQUE, pre_factor REAL, post_factor REAL, note TEXT);'''%(table_name)
        try:
            self.sqlite_cursor.execute(sql_str)
        except sqlite3.Error,e:
            print "create table failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
        
    def insert_stock_sub_table(self, table_name, records):
        sql_str='''INSERT OR IGNORE INTO %s(date, pre_factor, post_factor, note) values (?,?,?,?);'''%(table_name)
        try:
            self.sqlite_cursor.executemany(sql_str, records)
        except sqlite3.Error,e:
            print "insert records failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
        

    def create_SE_table(self):
        #create Stock Exchange table
        #交易所：上证，深证
        sql_str='''CREATE TABLE IF NOT EXISTS sh(i_index INTEGER PRIMARY KEY, code TEXT UNIQUE);'''
        try:
            self.sqlite_cursor.execute(sql_str)
        except sqlite3.Error,e:
            print "create table failed", "\n", e.args[0]
                     
        sql_str='''CREATE TABLE IF NOT EXISTS sz(i_index INTEGER PRIMARY KEY, code TEXT UNIQUE);'''
        try:
            self.sqlite_cursor.execute(sql_str)
        except sqlite3.Error,e:
            print "create table failed", "\n", e.args[0]
            
        self.sqlite_conn.commit()
        
    def insert_SE_record(self, records):        
        if records[0][0].find('sh') != -1:
            sql_str='''INSERT OR IGNORE INTO sh(code) values (?);'''
        else:
            sql_str='''INSERT OR IGNORE INTO sz(code) values (?);'''
        try:
            self.sqlite_cursor.executemany(sql_str, records)
        except sqlite3.Error,e:
            print "insert records failed", "\n", e.args[0]        
        self.sqlite_conn.commit()
        
    def close_db(self):
        self.sqlite_conn.close()

class RawDataParser(object):
    def __init__(self):
        pass    
    
    def parse_val(self, raw_data, val_name):
        ret_value = None
        pattern = ',%s:\d+'%(val_name)
        obj = re.search(pattern,raw_data)
        if obj:
            val_obj = re.search('[0-9]+', obj.group())
            ret_value = int(val_obj.group())
        return ret_value    
    
    def parse_code(self, raw_data):
        code_list = []
        code_str = raw_data[raw_data.find('data:')+6:-3]
        code_str = code_str.split(',')
        for item in code_str:
            code_list.append((item,))
        return code_list  
    
    def parse_daily_data(self, raw_data):
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
     
    def parse_sub_data(self, raw_data):
        sub_list = []
        all_data_str = raw_data[raw_data.find('=')+2:-2].split('^')
        for item in all_data_str:
            sub_list.append(tuple(item.split('~')))        
        return sub_list
    
class GetStockData(object):
    def __init__(self,db_name='stock.db'):
        self.db = DBClass(db_name)
        self.db.create_SE_table()
        self.parser = RawDataParser()
    
    def save_sh_stock(self):        
        sh_str = 'http://stock.gtimg.cn/data/view/rank.php?t=rankash/chr&p=%s&o=0&l=80&v=list_data' #上证
        all_sh_code = self.get_all_code(sh_str)        
        for item in all_sh_code:
            self.save_stock_data(item[0])
            
    def save_sz_stock(self):
        sz_str = 'http://stock.gtimg.cn/data/view/rank.php?t=rankasz/chr&p=%s&o=0&l=80&v=list_data' #深证
        all_sz_code = self.get_all_code(sz_str)
        for item in all_sz_code:
            self.save_stock_data(item[0])
            
    def save_stock_data(self, stock_name):
        self.get_stock_sub_data(stock_name)
        self.db.create_stock_daily_table(stock_name)
        year_list = range(90, 99+1)
        year_list.extend(range(00, 15+1))
        self.get_stock_data(stock_name, year_list)
        
    def get_all_code(self, url_str, db_flag=True):
        #获取股票代码
        code_list = []
        try:        
            raw_data = requests.get(url_str%(1)).content
        except:
            print 'requests.get error'
            return code_list
            
        code_list.extend(self.parser.parse_code(raw_data))
        total = self.parser.parse_val(raw_data, 'total')
        for i in xrange(2,total+1):
            try:
                raw_data = requests.get(url_str%(i)).content
            except:
                print 'requests.get error'
                continue                
            code_list.extend(self.parser.parse_code(raw_data))
        if db_flag == True:                 
            self.db.insert_SE_record(code_list)
        return code_list

    def get_stock_data(self, stock_name, year_list, db_flag=True):
        #获取某股票数据
        print 'getting data: %s'%(stock_name)
        data_list = []
        for year in year_list:
            url = 'http://data.gtimg.cn/flashdata/hushen/daily/%02d/%s.js'%(year, stock_name)
            try:
                raw_data = requests.get(url).content
            except:
                print 'requests.get error'
                continue
            if raw_data.find('404 Not Found') != -1:
                print 'Year %02d, stock %s, no data'%(year, stock_name)
                continue        
            data_list.extend(self.parser.parse_daily_data(raw_data)['data'])
        if db_flag == True and data_list:
            self.db.insert_stock_daily_record(stock_name, data_list)
        return data_list
    
    def get_stock_sub_data(self, stock_name, db_flag=True):
        sub_list = []
        self.db.create_stock_sub_table(stock_name+'_sub')
        url = 'http://data.gtimg.cn/flashdata/hushen/fuquan/%s.js'%(stock_name)
        try:
            raw_data = requests.get(url).content
        except:
            print 'requests.get error'
            return sub_list        
        if raw_data.find('404 Not Found') != -1:
            print 'stock %s, no data sub'%(stock_name)
            return sub_list
        sub_list = self.parser.parse_sub_data(raw_data)
        if db_flag == True and sub_list:
            self.db.insert_stock_sub_table(stock_name+'_sub', sub_list)
        return sub_list

if __name__ == '__main__':

#     url = 'https://jy.yongjinbao.com.cn/winner_gj/gjzq/exchange.action'
#     params = {
#         'CSRF_Token': 'undefined',
#         'timestamp': '0.602064706152305',
#         'request_id': 'mystock_405'
#     }    
#     raw_data = requests.session.get(url, params=params).content
#     parse_test()
    stock_name_list = ['sh000001', 'sz399001', 'sh000300']
    stock_obj = GetStockData()
    for stock_name in stock_name_list:
        stock_obj.save_stock_data(stock_name)
    stock_obj.save_sh_stock()
    stock_obj.save_sz_stock()
    