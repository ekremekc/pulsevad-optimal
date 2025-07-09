function [k1_opt, k2_opt] = optimize_k_values(...
    loads_small, displacements_small, ...
    loads_rest, displacements_rest, ...
    load_range1, load_range2, ...
    E_eff_layers, A_layers, EI_0, EI_inf, h, n, F, L, P_max)

    % --- Optimize k1 ---
    k1_opt = golden_section(@(k1) objective_k1(k1, ...
        E_eff_layers, A_layers, EI_0, EI_inf, h, n, F, ...
        k2_fixed(), P_max, L, load_range1, displacements_small), ...
        2e6, 4e6, 1e-3);
    
    % --- Optimize k2 ---
    k2_opt = golden_section(@(k2) objective_k2(k2, ...
        E_eff_layers, A_layers, EI_0, EI_inf, h, n, F, ...
        k1_opt, P_max, L, load_range2, displacements_rest), ...
        0.1e6, 0.2e6, 1e-5);
end

function mse = objective_k1(k1, E_eff_layers, A_layers, EI_0, EI_inf, ...
                            h, n, F, k2, P_max, L, load_range, exp_disp)
    [EI_eff, ~] = calc_ebs(E_eff_layers, A_layers, EI_0, EI_inf, ...
                           h, n, F, k1, k2, P_max, L);
    model_disp = calc_deflection(load_range, EI_eff, L, F);
    
    % Interpolate to match experimental load points
    model_interp = interp1(load_range, model_disp, load_range, 'linear', 'extrap');
    mse = mean((model_interp - exp_disp).^2);
end

function mse = objective_k2(k2, E_eff_layers, A_layers, EI_0, EI_inf, ...
                            h, n, F, k1, P_max, L, load_range, exp_disp)
    [~, EI_eff2] = calc_ebs(E_eff_layers, A_layers, EI_0, EI_inf, ...
                            h, n, F, k1, k2, P_max, L);
    model_disp = calc_deflection(load_range, EI_eff2, L, F);
    
    % Interpolate to match experimental load points
    model_interp = interp1(load_range, model_disp, load_range, 'linear', 'extrap');
    mse = mean((model_interp - exp_disp).^2);
end

function x_opt = golden_section(f, a, b, tol)
    gr = (sqrt(5) + 1) / 2;
    c = b - (b - a) / gr;
    d = a + (b - a) / gr;

    while abs(c - d) > tol
        if f(c) < f(d)
            b = d;
        else
            a = c;
        end
        c = b - (b - a) / gr;
        d = a + (b - a) / gr;
    end
    x_opt = (a + b) / 2;
end

function k2 = k2_fixed()
    k2 = 0.15e6;  % Placeholder value during k1 optimization
end
