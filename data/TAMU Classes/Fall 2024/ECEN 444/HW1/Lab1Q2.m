%%%%%%%%%%%%%%%%%%%%%%%%%% P2.17 Part a)    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x = [1, 1, 1, 1, 0]; h = [6, 5, 4, 3, 2, 1, 0];
y = conv(x, h);

% range for n
n = 0:length(y)-1;
% plot
stem(n, y, "filled");

%Plot titles
xlabel('n');
ylabel('y[n]');
title('L1.2 Part (a) - Convolution of x[n] and h[n]');

%%%%%%%%%%%%%%%%%%%%%%%%%%  P2.17 Part b)   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x = [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]; nx = [-2:8];
h = [0, 1, 1, 0, 0, 0, 0]; nh = [-5:1];

[y, ny] = conv_m(x, nx, h, nh);

% display
disp('y[n] = ');
disp(y);
disp('n :');
disp(ny);

% plot
stem(ny, y, 'filled');
xlabel('n');
ylabel('y[n]');
title('L1.2 Part (c) - Convolution of x[n] and h[n]');