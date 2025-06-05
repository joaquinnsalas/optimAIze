% define symbolic variables
syms s

A = [0, 1; -3, -4]; % matrix A

% calculate (sI - A)^-1
I = eye(size(A)); % declare the matrix size
invMatrix = inv(s*I - A);

% inverse laplace of matrix
ilaplaceA = ilaplace(invMatrix);

% show answer
disp('L^-1(sI - A)^-1 is:');
disp(ilaplaceA);



