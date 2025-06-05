%%%%%%%%%%%%%%%%%%%%    L2.2    %%%%%%%%%%%%%%%%%%%%

points = [1, 3, 7, 15, 50, 70]; % from textbook
w_c = pi / 15; % w_c1 = pi/25
omega = linspace(-2, 2); %range

% make a plot for each value of N
figure;
for idx = 1:length(points)
    N = points(idx);
    % equation for gibbs phenomenon
    gibbs = zeros(1, length(omega));
    for n = -N:N
        if n == 0 % handle when n is 0, not plotting
            gibbs = gibbs + (w_c / pi) * exp(-1j * omega * n);
        else 
            gibbs = gibbs + (sin(w_c * n) ./ (pi * n)) .* exp(-1j * omega * n);
        end
    end
    % subplots
    subplot(3, 2, idx);
    plot(omega, abs(gibbs));
    title(['N = ', num2str(N)]);
    xlabel('w');
    ylabel('Fourier Transform');
end