'''
@author: john
'''
import re
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
            if str_temp[0][0] == '9':
                str_temp[0] = '19'+str_temp[0]
            else:
                str_temp[0] = '20'+str_temp[0]
            data_item = (str_temp[0], float(str_temp[1]), float(str_temp[2]), 
                         float(str_temp[3]), float(str_temp[4]), float(str_temp[4]))
            all_data.append(data_item)
        daily_data['data'] = all_data
        #date    open    close    high    low    volume
        #100104 3289.75 3243.76 3295.28 3243.32 109447927    
        return daily_data
    
    def parse_real_data(self, raw_data):
        all_data_str = raw_data.split('~')
        all_data_str.pop()
        all_data_str.pop(0)
        return all_data_str
    
    def parse_market_state(self, raw_data):        
        if (raw_data.find('SH_close') != -1) and (raw_data.find('SZ_close') != -1):
            return False 
        elif (raw_data.find('SH_open') != -1) and (raw_data.find('SZ_open') != -1):
            return True
         
    def parse_sub_data(self, raw_data):
        sub_list = []
        all_data_str = raw_data[raw_data.find('=')+2:-2].split('^')
        for item in all_data_str:
            sub_list.append(tuple(item.split('~')))        
        return sub_list 
    