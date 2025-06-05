syms t

A = [0, 1; -3, -4];

% declare variable 
I = eye(size(A));  

% calculate (sI - A)^-1 again
inverse = inv(s*I - A);

% for loops for inverse laplace element-wise
for i = 1:size(A, 1)
    for j = 1:size(A, 2)
        ilaplaceMatrix(i, j) = ilaplace(inverse(i, j), t);
    end
end

% show answer
disp('L^-1(sI - A)^-1 is:');
disp(ilaplaceMatrix);


