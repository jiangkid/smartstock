function [ Return ] = calc_profit(pos,stock_price )
%CALC_PROFIT Summary of this function goes here
%   Detailed explanation goes here
Return=zeros(length(pos),1);
%�����ʽ�仯�����
trade_rate = 0.0003;%���׳ɱ�����Ϊ��������
% trade_rate = 0;%�޽��׳ɱ�
Return(1)=1;
for t=2:length(pos)
    %�ղ���û�������ź�
    if pos(t)==0 && pos(t-1)==0
        Return(t)=Return(t-1);
        continue;
    end
    %����
    if pos(t)==1 && pos(t-1)==0
        Return(t)=Return(t-1)*(1-trade_rate);
        continue;
    end
    %�ֲֲ����������ź�
    if pos(t)==1 && pos(t-1)==1
        Return(t)=Return(t-1)*(stock_price(t)/stock_price(t-1));
        continue;
    end
    %����
    if pos(t)==0 && pos(t-1)==1
        Return(t)=Return(t-1)*(stock_price(t)/stock_price(t-1))*(1-trade_rate);
        continue;
    end
end
end

