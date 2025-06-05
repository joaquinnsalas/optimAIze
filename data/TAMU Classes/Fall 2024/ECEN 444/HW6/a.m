h1 = [0.037829, -0.023849, -0.110624, 0.37740, 0.852699] % h'[n] coefficients
h2 = [-0.064539, -0.04069, 0.418092, 0.788485] % h~'[n] coefficients
[H1, w1] = freqz(h1, 1, 1024); % using freqz for h'[n]
[H2, w2] = freqz(h2, 1, 1024); % using freqz for h~'[n]

figure; % plots of magnitude and phase of h'[n]
plot(w1/pi, 20*log10(abs(H1))); 
title('Magnitdue 1');
xlabel('frequency');
ylabel('Magnitude in dB');
figure;
plot(w1/pi, angle(H1)); 
title('Phase 1');
xlabel('frequency');
ylabel('Phase in radians');

figure; % plots of magnitude and phase of h~'[n]
plot(w2/pi, 20*log10(abs(H2))); 
title('Magnitude 2');
xlabel('frequency');
ylabel('Magnitude in dB');
figure;
plot(w2/pi, angle(H2)); 
title('Phase 2');
xlabel('frequency');
ylabel('Phase in radians');

%%%%%%%%%%%%%%%%%%%%%%% Part (b)    %%%%%%%%%%%%%%%%%%%%%%%
h = circshift(h1, 4);       % shift by 4
htilde = circshift(h2, 3); % shift by 3

% plot this using stem function
figure;
stem(h, 'filled');
title('h[n] shifted');
xlabel('n');
ylabel('h[n]');

figure;
stem(htilde, 'filled');
title('h~[n] shifted');
xlabel('n');
ylabel('h~[n]');

%%%%%%%%%%%%%%%%%%%%%%% Part (c)    %%%%%%%%%%%%%%%%%%%%%%%

% plot the magnitude now
figure;
subplot(2,1,1);
plot(w2/pi, abs(H1)); 
title('H(e^{jw})');
xlabel('frequency');
ylabel('magnitude');

subplot(2,1,2);
plot(w2/pi, abs(H2)); 
title('H~(e^{jw})');
xlabel('frequency');
ylabel('magnitude');

%%%%%%%%%%%%%%%%%%%%%%% Part (c)    %%%%%%%%%%%%%%%%%%%%%%%

% find the sum
H_sum = abs(H1).^2 + abs(H2).^2;
figure;
plot(w1/pi, H_sum); % should equal 2
title('Sum');
xlabel('frequency');
ylabel('magnitude');
