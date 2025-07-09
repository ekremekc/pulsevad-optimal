function EI_eff = calc_EI_eff(E_eff_layers, A_layers, EI_0, EI_inf, ...
                               h, n, F, k1, P_max, L)
% CALC_EI_EFF calculates the effective bending stiffness (EI_eff)
% using the equations for symmetric 3-layer beams with slip for k1.
%
% Inputs:
%   E_eff_layers - Vector of effective Young's moduli for each layer
%   A_layers     - Vector of cross-sectional areas for each layer
%   EI_0         - Initial (reference) bending stiffness
%   EI_inf       - Fully bonded (infinite slip) bending stiffness
%   h            - Thickness of each layer (assumed equal)
%   n            - Number of layers (typically 3)
%   F            - Axial force (scalar)
%   k1           - Shear stiffness value for the first coupling case
%   P_max        - Maximum midspan load
%   L            - Span length
%
% Outputs:
%   EI_eff       - Effective bending stiffness for k1

    % Slip coefficients for symmetric case
    eta_1 = 1;
    eta_2 = 1;
    eta_0 = eta_1 + eta_2;

    % Axial stiffness of the outermost layer (layer n)
    EA_n = E_eff_layers(n) * A_layers(n);

    % Intermediate alpha^2 and beta^2 terms for k1
    alpha_sq = k1 * (((n-1)*h^2 / EI_0) + (2 / (EA_n * eta_0)));
    beta_sq  = (2 * k1 * EI_inf) / (EA_n * EI_0 * eta_0);

    % Compute lambda values for k1
    term_under_sqrt = (alpha_sq + F/EI_0)^2 - 4 * beta_sq * F / EI_inf;
    % Ensure non-negative discriminant
    term_under_sqrt = max(term_under_sqrt, 0);

    lambda_1 = sqrt(0.5 * (alpha_sq + F/EI_0) + 0.5 * sqrt(term_under_sqrt));
    lambda_2 = sqrt(0.5 * (alpha_sq + F/EI_0) - 0.5 * sqrt(term_under_sqrt));

    % Midspan deflection with slip (Eq. 32)
    term1_w_slip = (P_max * L) / (4 * F);

    if abs(lambda_1 - lambda_2) < 1e-9
        term2_w_slip = 0;
        term3_w_slip = 0;
    else
        term2_w_slip = (P_max/(2*F)) * ((F/EI_0 - lambda_2^2) / ...
                         (lambda_1 * (lambda_2^2 - lambda_1^2))) * tanh(lambda_1 * L / 2);
        term3_w_slip = (P_max/(2*F)) * ((F/EI_0 - lambda_1^2) / ...
                         (lambda_2 * (lambda_2^2 - lambda_1^2))) * tanh(lambda_2 * L / 2);
    end

    w_max_2 = term1_w_slip + term2_w_slip - term3_w_slip;

    % Max deflection without slip (Eq. 33)
    alpha_0 = sqrt(F / EI_inf);
    w_bar_max_2 = (P_max * L) / (4 * F) - (P_max / (2 * alpha_0 * F)) * tanh(alpha_0 * L / 2);

    % Deflection magnification factor (Eq. 34)
    delta_2 = w_max_2 / w_bar_max_2;

    % Final effective bending stiffness (Eq. 35)
    EI_eff = (1 / delta_2) * EI_inf;
end