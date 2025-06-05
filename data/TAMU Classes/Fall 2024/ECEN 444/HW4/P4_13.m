% Put in the coefficients
b0 = 2;
b1 = 3;
a1 = -1;
a2 = 0.81;

% Run through my function
[A_s, A_c, r, v_0] = invCCPP(b0, b1, a1, a2);
n=0;
xn_1 = A_c * r^n * cos(pi * v_0 * n) + A_s * r^n * sin(pi * v_0 * n); %equation from P4.12

%show answers
disp(['A_s = ', num2str(A_s), ', A_c = ', num2str(A_c), ', r = ', num2str(r), ', v_0 = ', num2str(v_0)]);
disp("Part 1");
disp(xn_1);

%%%%%%%%%%%%%%%%%%%%%%%%% Part 2 %%%%%%%%%%%%%%%%%%%%%%%%%

samples = 20;
xn = zeros(1, samples);

for n = 0:(samples)
    xn(n + 1) = A_c * r^n * cos(pi * v_0 * n) + A_s * r^n * sin(pi * v_0 * n); %equation from P4.12
end

disp("Part 2");
disp(xn);

