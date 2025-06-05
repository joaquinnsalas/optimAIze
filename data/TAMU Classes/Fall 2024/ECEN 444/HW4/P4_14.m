% Coefficients
b0 = [-2, 5.65, -2.88];
a0 = [1, -0.1, 0.09, 0.648];

% residuez to find partial fraction expansion
[ro, po, ko] = residuez(b0, a0);
%[bo, ao] = residuez(ri, pi, ki);

% Display the results
disp("ro: ");
disp(ro);
disp("po: ");
disp(po);
disp("ko: ");
disp(ko);

%%%%%%%%%%%%%%%%%%%%%%%%% Part 2 %%%%%%%%%%%%%%%%%%%%%%%%%

b0 = 1.0000 - 0.8660i;
b1 = -4.0000 + 0.0000i;
a1 = 0.4500 + 0.7794i;
a2 = -0.8000 + 0.0000i;

% call my function
[A_s, A_c, r, v_0] = invCCPP(b0, b1, a1, a2);

% show result
disp(['A_s = ', num2str(A_s)]);
disp(['A_c = ', num2str(A_c)]);
disp(['r = ', num2str(r)]);
disp(['v_0 = ', num2str(v_0)]);


