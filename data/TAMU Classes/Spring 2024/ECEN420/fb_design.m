function F = fb_design(poles)

    A = [-1, 0; 0, -3];  % system dynamics matrix
    B = [1/2; -1/2];          % input matrix
    
    % using the place function to compute the feedback matrix F
    F = place(A, B, poles);
    
end
