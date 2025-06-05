function yt = sys_response(sys, ut)

    % define the variables for laplace
    syms s t
    
    % take the laplace transform of the input function
    U_s = laplace(ut, t, s);
    
    % multiply the line above by the transfer function
    Y_s = sys * U_s;
    
    % taking the inverse laplace transform to find the output in time domain
    yt = ilaplace(Y_s, s, t);
end