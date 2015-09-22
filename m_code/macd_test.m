%%�˳�����������MACDָ�겢������Ч�Խ��лز����
%%ԭʼ��������Ϊstk_clpr���ҵ�һ��Ϊ���̼ۣ��ڶ���Ϊ��������
%% �������ָ��(����Ҳ�ɱ�һ������)����һ���ʼ����DIFF=DEA=MACD=0,EMAshort=EMAlong=��һ������̼�
%��Ȼmatlab���Դ��ĺ���macd()����ò��ֻ�ܼ���Ĭ�ϳ��ȵ�ƽ���ƶ�ƽ���������Լ����������
conn=database('stock.db','','','org.sqlite.JDBC','jdbc:sqlite:E:/workspace/smartstock/src/');
curs=exec(conn,'select date,close from sh000300');
curs=fetch(curs);
% clpr=stk_clpr(:,1);%��ȡ���̼�
% date=stk_clpr(:,2);%��ȡ����
clpr=cell2mat(curs.data(:,2));
date=datenum(cell2mat(curs.data(:,1)),'yymmdd');

% select data by date
start_date = '050921';%'yymmdd'
clpr = clpr(date>datenum(start_date,'yymmdd'));
date = date(date>datenum(start_date,'yymmdd'));

%������㳤��
shortPeriod=12;%�������̼۶��ڣ����٣�ƽ���ƶ�ƽ�����㳤��
longPeriod=26;%�������̼۳��ڣ����٣�ƽ���ƶ�ƽ�����㳤��
DEAPeriod=9;%����diff��ƽ���ƶ�ƽ�����㳤��
%����ռλ������߳�������Ч��
EMAshort=zeros(length(clpr),1);
EMAlong=zeros(length(clpr),1);
DIFF=zeros(length(clpr),1);
DEA=zeros(length(clpr),1);
MACD=zeros(length(clpr),1);
%��ѭ�����������ָ�꣨���������������ã�
EMAshort(1)=clpr(1);%��ʼ��EMAshort��һֵ
EMAlong(1)=clpr(1);%��ʼ��EMAlong��һ��ֵ
DEA(1)=0;%��ʼ����һֵ
DIFF(1)=0;
MACD(1)=0;
for t=2:length(clpr);
    %������ںͳ���EMA
    EMAshort(t)=clpr(t)*(2/(shortPeriod+1))+EMAshort(t-1)*((shortPeriod-1)/(shortPeriod+1));
    EMAlong(t)=clpr(t)*(2/(longPeriod+1))+EMAlong(t-1)*((longPeriod-1)/(longPeriod+1));
    %����DIFF
    DIFF(t)=EMAshort(t)-EMAlong(t);
    %����DEA
    DEA(t)=DIFF(t)*(2/(DEAPeriod+1))+DEA(t-1)*((DEAPeriod-1)/(DEAPeriod+1));
    %����MACD
    MACD(t)=2*(DIFF(t)-DEA(t));
end
% figure(10);
% plot(str2num(cell2mat(curs.data(:,1))),MACD,'r');
% date_macd = [str2num(cell2mat(curs.data(:,1))),MACD];
%������������ͼ�͸�ָ��仯ͼ
figure(1);
subplot(3,1,1);
plot(date,clpr,'r');
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('Close Price');
title('Time Series of Stock');
grid on;
subplot(3,1,2);
plot(date,DIFF,'g',date,DEA,'b');
datetick('x','yyyymmdd');
legend('DIFF','DEA');
xlabel('Date');
ylabel('DIFF and DEA');
title('The DIFF and DEA of Stock');
grid on;
subplot(3,1,3);
bar(date(MACD>0),MACD(MACD>0),'red');hold on;
bar(date(MACD<=0),MACD(MACD<=0),'green');hold off;
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('MACD');
title('The MACD of Stock');
grid on;
%% ���Իز����
%%һ����򵥵Ĳ��ԣ�1)DIFF����ͻ��MACD���������촦��MACD֮�ϣ���Ϊ�����źţ���)DIFF���´���MACD���������촦��MACD֮�£���Ϊ�����ź�
%��ʼ�ʽ�10000Ԫ
initial=10000;
%�����λ��1��ʾ��ͷ��0��ʾ�ղ�
pos=zeros(length(clpr),1);
%������������
Return=zeros(length(clpr),1);
figure(2);
subplot(2,1,1);
bar(date(MACD>0),MACD(MACD>0),'red');hold on;
bar(date(MACD<=0),MACD(MACD<=0),'green');hold off;
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('MACD');
title('The MACD of Stock');
grid on;
subplot(2,1,2);
plot(date,clpr,'r');
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('Close Price');
title('Time Series of Stock');
grid on;
hold on;
%���Լ���
for t=5:length(clpr)
    %���������ź�
%     signalBuy=(DIFF(t)>MACD(t) && DIFF(t-1)>MACD(t-1) && DIFF(t-2)>MACD(t-2) && DIFF(t-3)<MACD(t-3) && DIFF(t-4)<MACD(t-4)); 
%     signalSell=(DIFF(t)<MACD(t) && DIFF(t-1)<MACD(t-1) && DIFF(t-2)<MACD(t-2) && DIFF(t-3)>MACD(t-3) && DIFF(t-4)>MACD(t-4));
    signalBuy = (MACD(t)>0);
    signalSell = (MACD(t)<=0);
    %����������ź���Ϊ�ղ֣�������
    if (signalBuy==1 && pos(t-1)==0)
        pos(t)=1;
%         text(date(t),clpr(t),'\leftarrow��');
        plot(date(t),clpr(t),'go');

    %����������ź���Ϊ��֣�������
    elseif (signalSell==1 && pos(t-1)==1)
        pos(t)=0;
%         text(date(t),clpr(t),'\leftarrow��');
        plot(date(t),clpr(t),'bo');

    %�������һ�ɲ������κβ���
    else    pos(t)=pos(t-1);
    end
end
%�����ʽ�仯��������׳ɱ�����Ϊ����ǧ��֮��
Return = calc_profit(pos,clpr);
% Return(1)=initial;
% for t=2:length(clpr)
%     %�ղ���û�������ź�
%     if pos(t)==0 && pos(t-1)==0
%         Return(t)=Return(t-1);
%         continue;
%     end
%     %����
%     if pos(t)==1 && pos(t-1)==0
%         Return(t)=Return(t-1);%*(1-0.0003);
%         continue;
%     end
%     %�ֲֲ����������ź�
%     if pos(t)==1 && pos(t-1)==1
%         Return(t)=Return(t-1)*(clpr(t)/clpr(t-1));
%         continue;
%     end
%     %����
%     if pos(t)==0 && pos(t-1)==1
%         Return(t)=Return(t-1)*(clpr(t)/clpr(t-1));%*(1-0.0003);
%         continue;
%     end
% end
disp(Return(end));
%% ģ�����ۣ������ʣ����ձ��ʣ����������ʣ����س���һЩ��ָ�꣬����ֻ���ʽ�仯����
%�����ʽ�仯����
hold off;
figure(3);
plot(date,Return,'r');
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('Your Money');
title('The Return of Stock');
%�����ֲ����
figure(4);
plot(date,pos,'b');
datetick('x','yyyymmdd');
xlabel('Date');
ylabel('The state of your account');