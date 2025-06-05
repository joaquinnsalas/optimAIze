

% from example
f = [0 0.2 0.4 0.6 0.8 1]; % in w/pi unis
m = [0,0.1,0.4,0.6,1.2,1.5]; % magnitude values
h = firpm(25,f,m,'differentiator');
[db,mag,pha,grd,w] = freqz_m(h,[1]);
subplot(2,1,1); stem([0:25],h); title('Impulse Response');
xlabel('n’); ylabel(’h(n)'); axis([0,25,-0.6,0.6])
set(gca,'XTickMode’,’manual’,’XTick',[0,25])
set(gca,'YTickMode','manual','YTick',-0.6:0.2:0.6);
subplot(2,1,2); plot(w/(2*pi),mag); title('Magnitude Response')
xlabel('Normalized frequency f'); ylabel('|H|')
set(gca,'XTickMode','manual','XTick',f/2)
set(gca,'YTickMode','manual','YTick',[0,0.1,0.4,0.6,1.2,1.5]); grid

M = N + 1;
fprintf('filter order: %d\n', M);
fprintf('stopband attenuation: %.4f dB\n', Asd);

% plot
figure;
subplot(2,1,1);
plot(w/pi, db);
title('mag. response (dB)');
xlabel('normalized freq');
ylabel('magnitude');
subplot(2,1,2);
zerophase(h); % use zerophase
% error function
ideal_response = [ones(1, wp/delta_w), zeros(1, length(w) - wp/delta_w)];
error_function = abs(mag - ideal_response);
figure;
plot(w/pi, error_function);
title('error function');
xlabel('normalized freq');
ylabel('amplitude error');