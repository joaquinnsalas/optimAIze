%%%%%%%%%%%%%%%%%%%%%%%%%%  L1.1   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%    Figure 2.1.1    %%%%
figure;
x = [0.9, -0.8, 0.7, 1.5, 2, 1.7, 1.0, 0.7, -0.8, 1.2]; 
nx = -4:5;
stem(nx, x, 'filled');
title('Figure 2.1.1');
xlabel('n');
ylabel('x[n]');

%%%%    Figure 2.1.2    %%%%
figure;
x = [0,0,1,0,0,0,0];
stem(x, 'filled');
title('Figure 2.1.2');
xlabel('n');
ylabel('x[n]');

%%%%    Figure 2.1.3    %%%%
figure;
x = [0,0,0,1,1,1,1,1,1,1,1]; 
nx = -3:7;
stem(nx, x, 'filled');
title('Figure 2.1.3');
xlabel('n');
ylabel('x[n]');

%%%%    Figure 2.1.4    %%%%
figure;
nx = 0:10;
x = nx;
stem(nx, x, 'filled');
title('Figure 2.1.4');
xlabel('n');
ylabel('x[n]');

%%%%    Figure 2.1.5    %%%%
figure;
n = 0:10;
e = 2;
x = e.^n;
stem(n, x, 'filled');
title('Figure 2.1.5');
xlabel('n');
ylabel('x[n]');