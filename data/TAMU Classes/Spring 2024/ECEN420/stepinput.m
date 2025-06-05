    % Define variables
    syms t s
    
    % laplace of the input
    Us = laplace(ut, t, s);

    ut = sin(pi * t); % input is step
    sys = (s+1)/(s^2+5*s+6); 
    
    % system transfer function times the s-domain
    Ys = sys * Us;
    
    % ilaplace for the output in time domain
    yt = ilaplace(Ys, s, t);

    time = 0 : 0.01 : 5;
    y_sin = subs(yt, time);

    % plot output y(t)
    plot(time, y_sin)

    disp(yt)


