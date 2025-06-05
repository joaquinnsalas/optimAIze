function [A_s, A_c, r, v_0] = invCCPP(b0, b1, a1, a2)

    r = sqrt(a2);
    
    cos_v0 = -a1 / (2*r);
    
    sin_v0 = sqrt(1 - cos_v0^2);
    
    A_c = b0;
    
    A_s = (b1 + r * A_c * cos_v0) / (r * sin_v0);
    
    v_0 = acos(cos_v0) / pi;
end