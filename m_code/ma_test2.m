clear;
% close all;
stock_list = ['sh000300','sh000001','sz399001'];
conn=database('stock.db','','','org.sqlite.JDBC','jdbc:sqlite:E:/workspace/smartstock/src/');
curs=exec(conn,'select code from sh');
curs=fetch(curs);
all_stock_code = cell2mat(curs.data);
% close(conn);
% clpr=stk_clpr(:,1);%提取收盘价
% date=stk_clpr(:,2);%提取日期

%均线
ma_short = 5;
ma_middle = 60;
ma_long = 90;

results = zeros(length(all_stock_code),1);
results_max = zeros(length(all_stock_code),1);
for i = 1:length(all_stock_code)
    sql_str = sprintf('select date,close from %s order by date asc',all_stock_code(i,:));
    curs=exec(conn,sql_str);
    curs=fetch(curs);
    close_price=cell2mat(curs.data(:,2));
    all_date=datenum(cell2mat(curs.data(:,1)),'yyyymmdd');
    
    sql_str = sprintf('select date,pre_factor,post_factor from %s_sub order by date asc',all_stock_code(i,:));
    curs2=exec(conn,sql_str);
    curs2=fetch(curs2);
    if strcmp(curs2.data,'No Data') ~= 1
        close_price = sub_price(close_price, all_date, curs2.data);
    end

    MA_S = ma(close_price,ma_short);
    MA_M = ma(close_price,ma_middle);
    MA_L = ma(close_price,ma_long);
    pos = cal_pos(close_price, MA_S, MA_M, MA_L);%获取买卖信号
    profit_all = calc_profit(pos, close_price);
    results(i) = profit_all(end);
    results_max(i) = max(profit_all);
end
disp(max(results));%85
disp(max(results_max));
