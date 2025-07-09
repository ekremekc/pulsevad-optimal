function deflection = calc_deflection(p_vec, EI, L, F)
    % calc_deflection computes the deflection based on pressure vector and stiffness
    %
    % Inputs:
    %   p_vec - Pressure vector or scalar
    %   EI    - Flexural rigidity
    %   L     - Length of the beam
    %   F     - Axial force
    %
    % Output:
    %   deflection - Calculated deflection

    deflection = (p_vec * L) / (4 * F) ...
               - (p_vec ./ (2 * F * sqrt(F ./ EI))) .* tanh(sqrt(F ./ EI) * L / 2);
end