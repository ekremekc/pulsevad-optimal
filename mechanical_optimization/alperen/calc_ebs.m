function [EI_eff, EI_eff2] = calc_ebs(E_eff_layers, A_layers, EI_0, EI_inf, ...
                                      h, n, F, k1, k2, P_max, L)
% CALC_EBS calculates the effective bending stiffness (EI_eff and EI_eff2)
% using the equations for symmetric 3-layer beams with slip.
%
% Inputs:
%   E_eff_layers - Vector of effective Young's moduli for each layer
%   A_layers     - Vector of cross-sectional areas for each layer
%   EI_0         - Initial (reference) bending stiffness
%   EI_inf       - Fully bonded (infinite slip) bending stiffness
%   h            - Thickness of each layer (assumed equal)
%   n            - Number of layers (typically 3)
%   F            - Axial force (scalar)
%   k1, k2       - Shear stiffness values for two coupling cases
%   P_max        - Maximum midspan load
%   L            - Span length
%
% Outputs:
%   EI_eff       - Effective bending stiffness for k1
%   EI_eff2      - Effective bending stiffness for k2

    % Slip coefficients for symmetric case
    eta_1 = 1;
    eta_2 = 1;
    eta_0 = eta_1 + eta_2;

    % Axial stiffness of the outermost layer (layer n)
    EA_n = E_eff_layers(n) * A_layers(n);

    % Intermediate alpha^2 and beta^2 terms
    alpha_sq = k1 * (((n-1)*h^2 / EI_0) + (2 / (EA_n * eta_0)));
    beta_sq  = (2 * k1 * EI_inf) / (EA_n * EI_0 * eta_0);

    alpha_sq2 = k2 * (((n-1)*h^2 / EI_0) + (2 / (EA_n * eta_0)));
    beta_sq2  = (2 * k2 * EI_inf) / (EA_n * EI_0 * eta_0);

    % Compute lambda values for both stiffness scenarios
    term_under_sqrt = (alpha_sq + F/EI_0)^2 - 4 * beta_sq * F / EI_inf;
    term_under_sqrt2 = (alpha_sq2 + F/EI_0)^2 - 4 * beta_sq2 * F / EI_inf;

    % Ensure non-negative discriminants
    term_under_sqrt = max(term_under_sqrt, 0);
    term_under_sqrt2 = max(term_under_sqrt2, 0);

    lambda_1  = sqrt(0.5 * (alpha_sq + F/EI_0) + 0.5 * sqrt(term_under_sqrt));
    lambda_2  = sqrt(0.5 * (alpha_sq + F/EI_0) - 0.5 * sqrt(term_under_sqrt));
    lambda_12 = sqrt(0.5 * (alpha_sq2 + F/EI_0) + 0.5 * sqrt(term_under_sqrt2));
    lambda_22 = sqrt(0.5 * (alpha_sq2 + F/EI_0) - 0.5 * sqrt(term_under_sqrt2));

    % Midspan deflection with slip (Eq. 32)
    term1_w_slip = (P_max * L) / (4 * F);

    if abs(lambda_1 - lambda_2) < 1e-9
        term2_w_slip = 0;
        term3_w_slip = 0;
        term2_w_slip2 = 0;
        term3_w_slip2 = 0;
    else
        term2_w_slip  = (P_max/(2*F)) * ((F/EI_0 - lambda_2^2) / ...
                         (lambda_1 * (lambda_2^2 - lambda_1^2))) * tanh(lambda_1 * L / 2);
        term3_w_slip  = (P_max/(2*F)) * ((F/EI_0 - lambda_1^2) / ...
                         (lambda_2 * (lambda_2^2 - lambda_1^2))) * tanh(lambda_2 * L / 2);

        term2_w_slip2 = (P_max/(2*F)) * ((F/EI_0 - lambda_22^2) / ...
                         (lambda_12 * (lambda_22^2 - lambda_12^2))) * tanh(lambda_12 * L / 2);
        term3_w_slip2 = (P_max/(2*F)) * ((F/EI_0 - lambda_12^2) / ...
                         (lambda_22 * (lambda_22^2 - lambda_12^2))) * tanh(lambda_22 * L / 2);
    end

    w_max_2  = term1_w_slip + term2_w_slip  - term3_w_slip;
    w_max_22 = term1_w_slip + term2_w_slip2 - term3_w_slip2;

    % Max deflection without slip (Eq. 33)
    alpha_0 = sqrt(F / EI_inf);
    w_bar_max_2 = (P_max * L) / (4 * F) - (P_max / (2 * alpha_0 * F)) * tanh(alpha_0 * L / 2);

    % Deflection magnification factors (Eq. 34)
    delta_2  = w_max_2  / w_bar_max_2;
    delta_22 = w_max_22 / w_bar_max_2;

    % Final effective bending stiffness (Eq. 35)
    EI_eff  = (1 / delta_2)  * EI_inf;
    EI_eff2 = (1 / delta_22) * EI_inf;

end
