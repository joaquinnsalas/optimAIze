%%%%%%%%%%%%%%%%%%%%    L2.1    %%%%%%%%%%%%%%%%%%%%

w = linspace(-2*pi, 2*pi); % range for omega

% the equation for frequency response
H = (1/(0 + 5 + 1)) .* exp(-1j .* w .* (5 - 0) / 2) .* (sin(w .* (0 + 5 + 1) / 2) ./ sin(w / 2));
% for magnitude and the phase
magH = abs(H); 
phaseH = angle(H);
% plot
figure;
subplot(2,1,1);
plot(w, magH);
title('Magnitude');
xlabel('w');
ylabel('Function');

subplot(2,1,2);
plot(w, phaseH);
title('Phase');
xlabel('w');
ylabel('angle of funtion');
