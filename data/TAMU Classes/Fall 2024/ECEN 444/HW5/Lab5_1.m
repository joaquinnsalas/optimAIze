% I will be using grpdelay, a matlab function https://www.mathworks.com/help/signal/ref/grpdelay.html

% There are two values given for a
a1 = 0.4;
a2 = -0.4;
% Function H(z) for each value of a
b1 = [1 -conj(a1)];
a1bottom = [1 -a1];
b2 = [1 -conj(a2)];
a2bottom = [1 -a2];
% Neweded to set a range for omega
omega = linspace(-pi, pi);
%a = 0.4
figure;
subplot(3,1,1);
[H1, w] = freqz(b1, a1bottom, omega);
plot(w/pi, abs(H1));
title('magnitude response at a = 0.4');
xlabel('frequency');
ylabel('Magnitude');
subplot(3,1,2);
plot(w/pi, angle(H1));
title('phase response at a = 0.4');
xlabel('frequency');
ylabel('phase angle');
% Group delay using grpdelay
subplot(3,1,3);
[gd1, w] = grpdelay(b1, a1bottom, omega);
plot(w/pi, gd1);
title('group delay at a = 0.4');
xlabel('frequency');
ylabel('group delay');
%a = -0.4
figure;
subplot(3,1,1);
[H2, w] = freqz(b2, a2bottom, omega);
plot(w/pi, abs(H2));
title('magnitude response for a = -0.4');
xlabel('frequency');
ylabel('magnitude');
subplot(3,1,2);
plot(w/pi, angle(H2));
title('phase response at a = -0.4');
xlabel('frequency');
ylabel('phase angle');
subplot(3,1,3);
[gd2, w] = grpdelay(b2, a2bottom, omega);
plot(w/pi, gd2);
title('group delay at a = -0.4');
xlabel('frequency');
ylabel('group delay');