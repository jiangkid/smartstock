function [ Return ] = calc_profit(pos,stock_price )
%CALC_PROFIT Summary of this function goes here
%   Detailed explanation goes here
Return=zeros(length(pos),1);
%计算资金变化情况，
trade_rate = 0.0003;%交易成本假设为单边万三
% trade_rate = 0;%无交易成本
Return(1)=1;
for t=2:length(pos)
    %空仓且没有买入信号
    if pos(t)==0 && pos(t-1)==0
        Return(t)=Return(t-1);
        continue;
    end
    %买入
    if pos(t)==1 && pos(t-1)==0
        Return(t)=Return(t-1)*(1-trade_rate);
        continue;
    end
    %持仓并且无卖出信号
    if pos(t)==1 && pos(t-1)==1
        Return(t)=Return(t-1)*(stock_price(t)/stock_price(t-1));
        continue;
    end
    %卖出
    if pos(t)==0 && pos(t-1)==1
        Return(t)=Return(t-1)*(stock_price(t)/stock_price(t-1))*(1-trade_rate);
        continue;
    end
end
end

