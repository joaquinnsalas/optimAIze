b = [1, 2, 3];
a = 1;

figure;
freqz(b, a);

n = 0:200;  % 200 samples
x_n = sin(pi*n/2) + 5*cos(pi*n);
y_n = filter(b, a, x_n);

%plot
figure;
subplot(2, 1, 1);
plot(n, x_n);
xlabel('n');
ylabel('x(n)');

subplot(2, 1, 2);
plot(n, y_n);
xlabel('n');
ylabel('y(n)');
