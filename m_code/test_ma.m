clear;
% close all;
stock_list = ['sh000300','sh000001','sz399001'];
conn=database('stock.db','','','org.sqlite.JDBC','jdbc:sqlite:E:/workspace/smartstock/src/');
curs=exec(conn,'select date,close from sh000300');
curs=fetch(curs);
close(conn);
% clpr=stk_clpr(:,1);%提取收盘价
% date=stk_clpr(:,2);%提取日期
close_price=cell2mat(curs.data(:,2));
all_date=datenum(cell2mat(curs.data(:,1)),'yymmdd');

% 从最高点
[vale,idx] = max(close_price);
close_price = close_price(idx:end);
all_date = all_date(idx:end);

%最低点
% [vale,idx] = min(close_price);
% close_price = close_price(idx:end);
% all_date = all_date(idx:end);

% select data by date
% start_date = '090921';%'yymmdd'
% close_price = close_price(all_date>datenum(start_date,'yymmdd'));
% all_date = all_date(all_date>datenum(start_date,'yymmdd'));

end_date = '140528';%'yymmdd'
close_price = close_price(all_date<datenum(end_date,'yymmdd'));
all_date = all_date(all_date<datenum(end_date,'yymmdd'));

%均线
ma_short_list = [5,10,15,20,30,60];
ma_middle_list = [60,90,120,180];
ma_long_list = [90,120,180,250];

results = zeros(length(ma_short_list),length(ma_middle_list), length(ma_long_list));
results_max = zeros(length(ma_short_list),length(ma_middle_list), length(ma_long_list));
for S = 1:length(ma_short_list)
    for M = 1:length(ma_middle_list)
        parfor L = 1:length(ma_long_list)
            MA_S = ma(close_price,ma_short_list(S));
            MA_M = ma(close_price,ma_middle_list(M));
            MA_L = ma(close_price,ma_long_list(L));
            pos = cal_pos(close_price, MA_S, MA_M, MA_L);%获取买卖信号
            profit_all = calc_profit(pos, close_price);
            results(S,M,L) = profit_all(end);
            results_max(S,M,L) = max(profit_all);
        end
    end
end
disp(max(max(max(results))));
disp(max(max(max(results_max))));

MA_S = ma(close_price,5);
MA_M = ma(close_price,60);
MA_L = ma(close_price,90);
pos = cal_pos(close_price, MA_S, MA_M, MA_L);%获取买卖信号
Return = calc_profit(pos, close_price);
disp(Return(end));
% (Return(end)-Return(1))/Return(1);
figure(1);
subplot(211);
plot(all_date, close_price);
plot_pos( all_date, close_price, pos);
hold on;
plot(all_date, MA_S);
plot(all_date, ma(close_price,30));
plot(all_date, MA_M);
plot(all_date, MA_L);
hold off;
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('Close Price');
grid on;
% legend('Real','ma\_s','ma\_m','ma\_L','buy','sale','Location','northwest');
xlim([all_date(1),all_date(end)]);

subplot(212)
plot(all_date,Return,'r');
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('Your Money');
title('The Return of Stock');
xlim([all_date(1),all_date(end)]);
