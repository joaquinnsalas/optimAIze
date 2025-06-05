% parameters
lambda = 10.5; %lambda in meters
t = 2; %time in seconds

% x range
x = linspace(0, 2 * lambda, 1000);

% ocean wave function
Y = 1.5 * cos(0.5 * t - 0.6 * x - (pi/2));

% plot it
plot(x, Y, 'b');
xlabel('Position (m)');
ylabel('Wave Height (m)');
title('Ocean Wave Height at t = 2 s');
grid on;
hold on;
