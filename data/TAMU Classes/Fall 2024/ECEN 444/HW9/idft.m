function [x] = idft(X, N)
%IDFT Summary of this function goes here
%   computes the inverse discrete fourier transform of an inputted seq.
% initialize x which will hold the output
    x = zeros(1, N)
    
    % compute the idft
    for n = 0: N - 1
        for k = 0: N-1
            x(n+1) = x(n+1) + X(k+1) * exp(1j * 2 * pi * k * n / N);
        end
    end

    %finally normalize the output by dividing by N
    x = x / N;
end

