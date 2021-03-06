#encoding: utf-8
'''
@author: john
'''
import urllib2
import sqlite3
import sys
import logging.handlers
from RawDataParser import RawDataParser

class mylogger(logging.Logger):
    def __init__(self, LOG_FILE='temp.log', print_flag=1):
        self.print_flag = print_flag
        if LOG_FILE[-4:] != ".log":
            LOG_FILE = LOG_FILE + ".log"
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(message)s'        
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)        
        self.logger = logging.Logger('tst')
        self.logger.addHandler(handler)  # 
        self.logger.setLevel(logging.DEBUG)
        print >> sys.stderr, 'log file: '+LOG_FILE    
        self.logger.info('------log init------')
        
    def log(self, msg):
        if self.print_flag == 1:
            print msg
        self.logger.info(msg)
        
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
    
class GetStockData(object):
    def __init__(self,db_name='stock.db'):
        self.logger = mylogger('stock.log')
        self.db = DBClass(db_name)
        self.db.create_SE_table()
        self.parser = RawDataParser()
        
    def log(self, msg):
        self.logger.log(msg)
        
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
            r = urllib2.urlopen(url_str%(1))
            raw_data = r.read()
#             raw_data = requests.get(url_str%(1)).content
        except:
            self.log('requests.get error')
            return code_list
            
        code_list.extend(self.parser.parse_code(raw_data))
        total = self.parser.parse_val(raw_data, 'total')
        for i in xrange(2,total+1):
            try:
                r = urllib2.urlopen(url_str%(i))
                raw_data = r.read()                
#                 raw_data = requests.get(url_str%(i)).content
            except:
                self.log('requests.get error')
                continue                
            code_list.extend(self.parser.parse_code(raw_data))
        if db_flag == True:                 
            self.db.insert_SE_record(code_list)
        return code_list

    def get_stock_data(self, stock_name, year_list, db_flag=True):
        #获取某股票数据
        self.log('getting data: %s'%(stock_name))
        data_list = []
        for year in year_list:
            url = 'http://data.gtimg.cn/flashdata/hushen/daily/%02d/%s.js'%(year, stock_name)
            try:                
                r = urllib2.urlopen(url)
                raw_data = r.read()
#                 raw_data = requests.get(url).content
            except:
                self.log('stock %s, requests.get error'%(stock_name))
                continue
            if raw_data.find('404 Not Found') != -1:
                self.log('Year %02d, stock %s, no data'%(year, stock_name))
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
            r = urllib2.urlopen(url)
            raw_data = r.read()    
#             raw_data = requests.get(url).content
        except:
            self.log('stock %s, requests.get error'%(stock_name))
            return sub_list        
        if raw_data.find('404 Not Found') != -1:
            self.log('stock %s, sub, no data'%(stock_name))
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
#     stock_obj.save_sh_stock()
#     stock_obj.save_sz_stock()
#     