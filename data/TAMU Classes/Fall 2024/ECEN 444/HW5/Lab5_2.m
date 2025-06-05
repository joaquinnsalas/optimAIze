%low-pass filter h[n] values
h = [(1+sqrt(3))/(4*sqrt(2)), (3+sqrt(3))/(4*sqrt(2)), (3-sqrt(3))/(4*sqrt(2)), (1-sqrt(3))/(4*sqrt(2))];
g = (-1).^(0:3) .* h; %high-pass filter g[n]
omega = linspace(-pi, pi);

% using freqz finding the frequency response for all values of h and g
[H, w] = freqz(h, 1, omega);
[G, w] = freqz(g, 1, omega);

% (a) plotting magnitude log and phase
figure;
subplot(2,1,1);
title('Plot of log Magnitude');
plot(w/pi, 20*log10(abs(H)));
plot(w/pi, 20*log10(abs(G)));

subplot(2,1,2);
title('Plot of Phase');
plot(w/pi, angle(H));
plot(w/pi, angle(G));

% (b) should equal 2
H_shifted = freqz(h, 1, omega + pi);
sum = abs(H).^2 + abs(H_shifted).^2; % add toghether and square
% plot
figure;
plot(w/pi, sum);
title('Part (b)');
xlabel('frequency');
ylabel('w^2');