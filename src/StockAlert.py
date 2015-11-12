#encoding:utf8
'''
@author: john
'''
import time
import urllib2
from RawDataParser import RawDataParser
class StockAlert(object):
    def __init__(self):
        self.parser = RawDataParser()
        self.year = int(time.strftime("%y", time.localtime()))
        
    def get_daily_data(self):
        #此函数已废弃，用get_market_data代替
        stock_data = self.get_stock_data('sh000001', [self.year])
        pre_close = stock_data[-2][2]
        cur_close = stock_data[-1][2]
        msg_title = u'%s'%stock_data[-1][0]
        msg = u'上证:%.2f(+%.2f)'%(cur_close, (cur_close-pre_close)/pre_close*100)        
        
        stock_data = self.get_stock_data('sz399001', [self.year])
        pre_close = stock_data[-2][2]
        cur_close = stock_data[-1][2]
        msg = msg + u' 深证:%.2f(+%.2f)'%(cur_close, (cur_close-pre_close)/pre_close*100)
        
        stock_data = self.get_stock_data('sz399006', [self.year])
        pre_close = stock_data[-2][2]
        cur_close = stock_data[-1][2]
        msg = msg + u' 创业板:%.2f(+%.2f)'%(cur_close, (cur_close-pre_close)/pre_close*100)
        return(msg_title, msg)
        
    def get_market_data(self, market_stock=['sh000001', 'sz399001', 'sz399006', 'sh000300']):        
        market_data = []
        for stock_name in market_stock:
            market_data.append(self.get_real_data(stock_name))
        msg = u'上证:%s(%s%%)'%(market_data[0][2], market_data[0][4])
        msg = msg + u' 深成:%s(%s%%)'%(market_data[1][2], market_data[1][4])
        msg = msg + u' 创业板:%s(%s%%)'%(market_data[2][2], market_data[2][4])
        msg = msg + u' 沪深300:%s(%s%%)'%(market_data[3][2], market_data[3][4])
        state = self.get_market_state()
        return (state, msg)
    
    def calc_ma(self,stock_name='sh000300'):
        today = time.strftime("%y%m%d", time.localtime())
        year_list = range(90, 99+1)
        year_list.extend(range(00, self.year+1))
        data_list = self.get_stock_data(stock_name, year_list)
        price_list = []
        for item in data_list:
            price_list.append(item[2])
        if data_list[-1][0] != today: #data is not update, add it
            real_data = self.get_real_data(stock_name)
            price_list.append(float(real_data[2]))            
        MA5 = self.MA(price_list, 5)
        MA60 = self.MA(price_list, 60)
        if(MA5[-1]>MA60[-1]):        
            msg = u'沪深300: MA5(%.2f)>MA60(%.2f)[买入]'%(MA5[-1], MA60[-1])
        else:
            msg = u'沪深300: MA5(%.2f)<MA60(%.2f)[买入]'%(MA5[-1], MA60[-1])
        return (msg, MA5, MA60)
    
    def MA(self, x, n):
        y = x[:]
        for t in xrange(len(x)):
            if t<n:
                y[t] = sum(x[0:t+1])/len(x[0:t+1])
            else:
                y[t] = sum(x[t-n+1:t+1])/len(x[t-n+1:t+1])       
        return y
    
    def get_market_state(self):
        url = 'http://qt.gtimg.cn/q=marketStat'
        try:                
            r = urllib2.urlopen(url)
            raw_data = r.read()
        except:
            return None
        return self.parser.parse_market_state(raw_data)

        
    def get_real_data(self, stock_name, short_flag=True):
        if short_flag is True:
            stock_name = 's_' + stock_name 
        url = 'http://qt.gtimg.cn/q=%s'%(stock_name)
        try:                
            r = urllib2.urlopen(url)
            raw_data = r.read()
        except:
            return None
        if raw_data.find('404 Not Found') != -1:
            return None
        return self.parser.parse_real_data(raw_data)
    
    def get_stock_data(self, stock_name, year_list):
        #获取某一年的数据
        data_list = []
        for year in year_list:
            url = 'http://data.gtimg.cn/flashdata/hushen/daily/%02d/%s.js'%(year, stock_name)
            try:                
                r = urllib2.urlopen(url)
                raw_data = r.read()
            except:
                continue
            if raw_data.find('404 Not Found') != -1:
                continue
            data_list.extend(self.parser.parse_daily_data(raw_data)['data'])
        return data_list
    
    def get_stock_sub_data(self, stock_name):
        sub_list = []
        url = 'http://data.gtimg.cn/flashdata/hushen/fuquan/%s.js'%(stock_name)
        try:
            r = urllib2.urlopen(url)
            raw_data = r.read()    
        except:
            return sub_list        
        if raw_data.find('404 Not Found') != -1:
            return sub_list
        sub_list = self.parser.parse_sub_data(raw_data)
        return sub_list
    
if __name__ == '__main__':
    year = int(time.strftime("%y", time.localtime()))
    stock_name = 'sh000001'
    stock_obj = StockAlert()
    msg = stock_obj.calc_ma()
    market_data = stock_obj.get_market_data()
    sub_data = stock_obj.get_stock_sub_data(stock_name)
    year_list = range(90, 99+1)
    year_list.extend(range(00, year+1))
    data_list = stock_obj.get_stock_data(stock_name, year_list)
    pass  

