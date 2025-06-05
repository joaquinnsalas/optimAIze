dielec = readmatrix('Dielectric_constant_data');

disp(dielec(17,1)); % for group 17, output - 26.0842 GHz
disp(dielec(17,2)); % output - 32.8947 (dielectric constant)

frequency = dielec(:,1); % first column is frequency
dielectric_constant = dielec(:,2); % second is dielectric constant

% plot
figure;
plot(frequency, dielectric_constant);

% labels
xlabel('Frequency (GHz)');
ylabel('Dielectric Constant');
title('Dielectric Constant of material X as a function of Frequency');
grid on;

