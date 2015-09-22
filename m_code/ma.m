function [ y ] = ma( x, n )
%MA Summary of this function goes here
%   Detailed explanation goes here
y = x;
for t = 1:length(x)
    if t<=n
        y(t) = mean(x(1:t));
    else
        y(t) = mean(x(t-n:t));
    end
end

end

