function [ pos ] = cal_pos( close_price, MA_S, MA_M, MA_L )
%�����λ��1��ʾ��ͷ��0��ʾ�ղ�
pos=zeros(length(close_price),1);
%���Լ���
for t=5:length(close_price)
    %���������ź�
    signalBuy = (MA_S(t)>=MA_M(t)) && (MA_M(t)>=MA_L(t));
    signalSell = (MA_S(t)<MA_M(t)) && (MA_M(t)<MA_L(t));
    
%     signalBuy = (MA_S(t)>=MA_M(t));
%     signalSell = (MA_S(t)<MA_M(t));
    
    %����������ź���Ϊ�ղ֣�������
    if (signalBuy==1 && pos(t-1)==0)
        pos(t)=1;
    %����������ź���Ϊ��֣�������
    elseif (signalSell==1 && pos(t-1)==1)
        pos(t)=0;
    %�������һ�ɲ������κβ���
    else
        pos(t)=pos(t-1);
    end
end

end

