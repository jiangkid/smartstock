function [  ] = plot_pos( date, price, pos )
%PLOT_POS Summary of this function goes here
%   Detailed explanation goes here
hold on;
for t=2:length(price)
    if (pos(t-1)==0 && pos(t)==1)
        plot(date(t),price(t),'ro');%buy
    elseif (pos(t-1)==1 && pos(t)==0)
        plot(date(t),price(t),'go');%sale
    end
end
hold off;
end

