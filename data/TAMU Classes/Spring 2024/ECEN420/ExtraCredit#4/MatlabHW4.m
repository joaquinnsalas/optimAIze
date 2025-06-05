K = 25000; % used in order to achieve Kv > 100
G = tf(K, conv([1, 0], conv([50, 1], [5, 1])));
D = tf([1/0.2, 1], [1/0.01, 1]);
Gc = series(D, G);
T = feedback(Gc, 1);
t = 0:0.01:10; % time range
r = t; % ramp input
[y, t] = lsim(T, r, t);


figure;
plot(t, r, 'b', t, y, 'r');
xlabel('time in seconds');
ylabel('output');
title('response to unit ramp input');
[Gm, Pm, Wcg, Wcp] = margin(Gc);
disp(['PM: ', num2str(Pm), ' degrees']);
