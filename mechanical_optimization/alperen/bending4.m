% MATLAB Code for Bending Stiffness of a 7-Wire Strand
% Implements the method from Zhang et al. (2018)
% "Bending Stiffness of Parallel Wire Cables Including Interfacial Slips among Wires"

clear; clc; close all;
load hm3_data.mat
loads = mean([load_1' load_2' load_3'],2);
displacements = mean([disp_1' disp_2' disp_3'],2);
loads = loads(2:end);
displacements = displacements(2:end);
%% 1. User-Defined Parameters
% Define the material, geometric, and loading properties.

% --- Geometry
d_wire = 0.0008; % Wire Diameter (m)

% --- Material Properties
E_center = 3e8; % Elasticity Modulus of the central wire (Pa)
E_outer = 10e9;  % Elasticity Modulus of the outer wires (Pa)

% --- Experimental Setup
L = 96/1000; % Cable Span (m) for simply supported beam setup
F = 1e-6; % Axial Tensile Force (N)

%% 2. Geometry Calculation based on Hexagonal Packing
% For a 7-wire strand, there is 1 central wire and 6 outer wires.

r_wire = d_wire / 2;
A_wire = pi * r_wire^2;

%% 3. Laminated Beam Idealization (as per the referenced paper)
% The cross-section is idealized into 3 rectangular layers.
% - Layer 1 (top): 2 outer wires
% - Layer 2 (middle): 1 central wire + 2 outer wires
% - Layer 3 (bottom): 2 outer wires

H = d_wire * (1 + sqrt(3)); % Total height of the section
n = 3; % Number of layers
h = H / n; % Height of each idealized layer

A_layer1 = 2 * A_wire;
A_layer2 = 3 * A_wire;
A_layer3 = 2 * A_wire;
A_layers = [A_layer1; A_layer2; A_layer3];

b_layers = A_layers / h; % Equivalent width of each layer

%% 4. Layer Stiffness and Limiting Bending Stiffness (EI_0 and EI_inf)

% --- Effective Elastic Modulus for each layer (Pa)
E_eff_layer1 = E_outer;
E_eff_layer2 = (E_center * A_wire + E_outer * 2 * A_wire) / (3 * A_wire);
E_eff_layer3 = E_outer;
E_eff_layers = [E_eff_layer1; E_eff_layer2; E_eff_layer3];

% --- Moment of Inertia for each idealized RECTANGULAR layer (m^4)
I_rect_layers = (b_layers .* h^3) / 12;

% --- Bending stiffness (EI) of each idealized layer (Nm^2)
EI_layers = E_eff_layers .* I_rect_layers;

% --- Full-Slip Bending Stiffness, EI_0 (Nm^2)
EI_0 = sum(EI_layers);

% --- No-Slip (Perfect Bonding) Bending Stiffness, EI_inf (Nm^2)
y_centroids = [2.5*h; 1.5*h; 0.5*h]; % From bottom of section
EA_products = E_eff_layers .* A_layers;
y_bar = sum(EA_products .* y_centroids) / sum(EA_products);
d_parallel_axis = y_centroids - y_bar;
parallel_axis_terms = EA_products .* (d_parallel_axis.^2);
EI_inf = EI_0 + sum(parallel_axis_terms);

%% 6. Calculating EBC
% --- Slip Parameter
% This is a crucial parameter that must be calibrated from experiments.
% See Fig. 6 in the reference paper for guidance (k = 7.26*sigma + 46.5).
k1 = 3;
k2 = 0.15; % Slip Rigidity (MPa), converted to Pa in the script
k1 = k1 * 1e6; % Convert MPa to Pa
k2 = k2 * 1e6;

% Define a range of forces for the plot
P_max = 2;  % Maximum Concentrated force at midspan (N) for plotting
P_range = linspace(0, P_max, 100);
P_range1 = linspace(0, 0.2, 100);
P_range2 = linspace(0.2, P_max, 100);
% 
% [EI_eff, EI_eff2] = calc_ebs(E_eff_layers, A_layers, EI_0, EI_inf, ...
%                              h, n, F, k1, k2, P_max, L);

EI_eff = calc_EI_eff(E_eff_layers, A_layers, EI_0, EI_inf, ...
                            h, n, F, k1, P_max, L);

EI_eff2 = calc_EI_eff(E_eff_layers, A_layers, EI_0, EI_inf, ...
                            h, n, F, k2, P_max, L);

deflection_eff = calc_deflection(P_range1, EI_eff, L, F);
deflection_eff2 = calc_deflection(P_range2, EI_eff2, L, F);

%% 7. Plot Load-Deflection Curves
disp('--- Generating Plot ---');

deflection_inf = calc_deflection(P_range, EI_inf, L, F);
deflection_0 = calc_deflection(P_range, EI_0, L, F);
% Create the plot
figure;
plot(deflection_inf * 1000, P_range, 'b--', 'LineWidth', 1.5);
hold on;
plot(deflection_eff * 1000, P_range1, 'r-', 'LineWidth', 2);
plot(deflection_eff2 * 1000-1.46, P_range2, 'r--', 'LineWidth', 2);
plot(deflection_0 * 1000, P_range, 'g--', 'LineWidth', 1.5);
plot(displacements, loads, '-o', 'LineWidth', 1)
hold off;
% Formatting
title('Load-Deflection Curve for 7-Wire Strand');
xlabel('Midspan Deflection (mm)');
ylabel('Concentrated Load (N)');
legend('No-Slip (EI_{inf})', 'Effective (EI_{eff})', 'Effective (EI_{eff2})','Full-Slip (EI_0)', 'Experimental', 'Location', 'southeast');
grid on;
set(gca, 'FontSize', 12);