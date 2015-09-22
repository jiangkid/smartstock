function [ pos ] = cal_pos( close_price, MA_S, MA_M, MA_L )
%定义仓位：1表示多头，0表示空仓
pos=zeros(length(close_price),1);
%策略计算
for t=5:length(close_price)
    %定义买卖信号
    signalBuy = (MA_S(t)>=MA_M(t)) && (MA_M(t)>=MA_L(t));
    signalSell = (MA_S(t)<MA_M(t)) && (MA_M(t)<MA_L(t));
    
%     signalBuy = (MA_S(t)>=MA_M(t));
%     signalSell = (MA_S(t)<MA_M(t));
    
    %如果是买入信号且为空仓，则买入
    if (signalBuy==1 && pos(t-1)==0)
        pos(t)=1;
    %如果是卖出信号且为多仓，则卖出
    elseif (signalSell==1 && pos(t-1)==1)
        pos(t)=0;
    %其它情况一律不进行任何操作
    else
        pos(t)=pos(t-1);
    end
end

end

