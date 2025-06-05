h = circshift(h_prime, 4);       % shift by 4
h_tilde = circshift(h_tilde_prime, 3); % shift by 3

% plot this using stem function
figure;
stem(h, 'filled');
title('h[n] shifted');
xlabel('n');
ylabel('h[n]');

figure;
stem(h_tilde, 'filled');
title('h~[n] shifted');
xlabel('n');
ylabel('h~[n]');