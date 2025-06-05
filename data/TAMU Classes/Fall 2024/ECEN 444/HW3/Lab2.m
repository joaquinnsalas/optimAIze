for i = 1:16
    X(i) = 1 - (i-1)/16;
end
for i = 17:240
    X(i) = 0;
end
for i = 241:256
    X(i) = (i-241)/16;
end
x = ifft(X, 256);

%%%%%%%%%%%%%%%%%%%% Part (a) %%%%%%%%%%%%%%%%%%%%

% down-sample every other point
y1 = zeros(size(x));
y1(1:2:end) = x(1:2:end);  %keeping every other sample
Y1 = fft(y1, 256); % take fourier transform
omega = linspace(0, 2*pi, 256);
%plot
figure;
title('Sampler Sequence');
plot(omega/pi, abs(Y1));
xlabel('frequency in pi');
ylabel('Y_1(omega)');

%%%%%%%%%%%%%%%%%%%% Part (b) %%%%%%%%%%%%%%%%%%%%
% take every other sample
y2 = x(1:2:256);
% tkae fourier transform
Y2 = fft(y2, length(y2));
omega2 = linspace(0, 2*pi, length(Y2));

figure;
plot(omega2/pi, abs(Y2));
xlabel('frequency in pi');
ylabel('Y_2(omega)');
title('Compressor Sequence');

%%%%%%%%%%%%%%%%%%%% Part (c) %%%%%%%%%%%%%%%%%%%%
% using zero padding
y3 = zeros(1, 2*length(x));
y3(1:2:end) = x;
Y3 = fft(y3, length(y3)); %fourier transform
omega3 = linspace(0, 2*pi, length(Y3));

figure;
plot(omega3/pi, abs(Y3));
xlabel('frequency in pi');
ylabel('Y_3(omega)');
title('Expander Sequence');
