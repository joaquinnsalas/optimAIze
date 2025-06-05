%%%%%%%%%%%%%%%%%%%%%%%%%%  P2.18   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x = [0, 1/3, 2/3, 1, 4/3, 5/3, 2]; nx = [0:6];
h = [0, 1, 1, 1, 1, 1, 0]; nh = [-3:3];

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