function [ price_out ] = sub_price( price, date, date_factors, flag )
%SUB_PRICE Summary of this function goes here
%   Detailed explanation goes here
if nargin<4
    flag = 1; %default
end
M = size(date_factors,1);
date_idx = zeros(M,1);
for idx = 1:M
    date_item = datenum(date_factors(idx,1),'yyyymmdd');
    [date_idx(idx),~] = find(date==date_item);
end
factors = cell2mat(date_factors(:,2:3));

price_out = price;
if flag == 1
    for i = 1:M
        price_out(1:date_idx(i)) = price_out(1:date_idx(i))*factors(i,1);
    end
elseif flag == 2
    for i = 1:M
        price_out(date_idx(i):end) = price_out(date_idx(i):end)*factors(i,2);
    end
end
end
