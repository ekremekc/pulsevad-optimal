function mse_total = objective_k1k2(k, loads1, disp1, loads2, disp2, ...
                                    E_eff_layers, A_layers, EI_0, EI_inf, ...
                                    h, n, F, L, P_max)
    k1 = k(1);
    k2 = k(2);
    
     % Penalize if k1 or k2 is non-positive
    if k1 <= 0 || k2 <= 0
        mse_total = 1e12;  % large penalty
        return;
    end
    
    [EI1, EI2] = calc_ebs(E_eff_layers, A_layers, EI_0, EI_inf, ...
                          h, n, F, k1, k2, P_max, L);

    model1 = calc_deflection(loads1, EI1, L, F);
    model2 = calc_deflection(loads2, EI2, L, F);

    mse1 = mean((model1 - disp1).^2);
    mse2 = mean((model2 - disp2).^2);

    mse_total = mse1 + mse2;
end