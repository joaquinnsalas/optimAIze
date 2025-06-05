function poles = MatlabHW3(num, den)
    % get the transfer function ready for inputs
    G = tf(num, den);
    
    % use feedback instead of the actual equation
    T = feedback(G, 1);
    
    % finding the poles of the closed-loop system
    poles = pole(T);

    disp('The poles of the closed-loop system:'); % display result
    disp(poles);
end
