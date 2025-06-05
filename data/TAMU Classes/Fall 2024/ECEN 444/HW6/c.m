% Frequency response for h[n] and h~[n]
[H, w_h] = freqz(h, 1, 1024);
[H_tilde, w_h_tilde] = freqz(h_tilde, 1, 1024);

% Plot magnitude responses of H(e^jw) and H~(e^jw)
figure;
subplot(2,1,1);
plot(w_h/pi, abs(H)); 
title('Magnitude Response of H(e^{jw})');
xlabel('Normalized Frequency (\times \pi rad/sample)');
ylabel('Magnitude');
grid on;

subplot(2,1,2);
plot(w_h_tilde/pi, abs(H_tilde)); 
title('Magnitude Response of H~(e^{jw})');
xlabel('Normalized Frequency (\times \pi rad/sample)');
ylabel('Magnitude');
grid on;