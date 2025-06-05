% constants needed
sigma = 4;  %conductivity
u = (1) * (4*pi*1e-7); % relivate mu r
%E = (8.854e-12) * (80); % relitave epsilon

% frequency range from 1k to 10GHz
f = logspace(3, 10, 1000); % 1000 specifies the amount of points
w = 2*pi*f; % calculating omega

% skin depth equation
S = sqrt(2 ./ (w * u * sigma));

figure;
loglog(f, S);
grid on;

xlabel('Frequency (Hz)');
ylabel('Skin Depth (m)');
title('Skin Depth vs. Frequency for Seawater');