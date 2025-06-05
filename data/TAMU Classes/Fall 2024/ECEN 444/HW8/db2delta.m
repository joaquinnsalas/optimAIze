function [delta1,delta2] = db2delta(Rp,As);
t=10^(Rp/20);
delta1=(t-1)/(1+t);
delta2=(1+delta1)*(10^(-As/20));
end

