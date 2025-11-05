"""
Parameter Estimation Analysis
By Josephina Kim (JK)

This shows detailed step-by-step parameter estimation calculations.
Perfect for understanding how we derive θ, μ, and σ from the data.
"""

import numpy as np
import matplotlib.pyplot as plt
from ou_process import OUProcess
from ou_estimator import OUEstimator
from trading_strategy import MeanReversionStrategy


def detailed_parameter_analysis(data, dt=1.0, true_params=None):
    estimator = OUEstimator()
    
    print("\n" + "="*70)
    print("DETAILED PARAMETER ESTIMATION ANALYSIS")
    print("="*70)
    
    print("\n1. AUTOCORRELATION ANALYSIS")
    print("-"*70)
    rho = estimator.estimate_autocorrelation(data, lag=1)
    print(f"Lag-1 Autocorrelation (ρ): {rho:.6f}")
    
    if rho > 0 and rho < 1:
        print(f"Mean reversion indicator: ρ < 1 (✓ Mean reverting)")
    else:
        print(f"Mean reversion indicator: ρ = {rho:.6f} (✗ May not be mean reverting)")
    
    print("\n2. THETA (θ) ESTIMATION - Mean Reversion Speed")
    print("-"*70)
    theta = estimator.estimate_theta_from_autocorr(data, dt)
    print("Formula: θ = -ln(ρ) / Δt")
    print(f"Calculation: θ = -ln({rho:.6f}) / {dt}")
    print(f"Estimated Theta (θ): {theta:.6f}")
    
    if true_params:
        theta_error = abs(theta - true_params['theta']) / true_params['theta'] * 100
        print(f"True Theta: {true_params['theta']:.6f}")
        print(f"Estimation Error: {theta_error:.2f}%")
    
    half_life = np.log(2) / theta if theta > 0 else None
    if half_life:
        print(f"Half-life: {half_life:.4f} time steps")
        print(f"Interpretation: Process reverts halfway to mean in {half_life:.2f} steps")
    
    print("\n3. MU (μ) ESTIMATION - Long-term Mean")
    print("-"*70)
    mu = estimator.estimate_mu(data)
    print("Formula: μ = (1/n) Σ X_i")
    print(f"Sample size: {len(data)}")
    print(f"Estimated Mu (μ): {mu:.6f}")
    
    if true_params:
        mu_error = abs(mu - true_params['mu']) / abs(true_params['mu']) * 100
        print(f"True Mu: {true_params['mu']:.6f}")
        print(f"Estimation Error: {mu_error:.2f}%")
    
    print("\n4. SIGMA (σ) ESTIMATION - Volatility")
    print("-"*70)
    sigma = estimator.estimate_sigma_from_theta(data, theta, mu, dt)
    print("Formula: σ² = (2θ / [n(1-e^(-2θΔt))]) Σ [X_{i+1} - X_i - μ(1-e^(-θΔt))]²")
    
    exp_neg_theta_dt = np.exp(-theta * dt)
    exp_neg_2theta_dt = np.exp(-2 * theta * dt)
    print("Intermediate values:")
    print(f"  e^(-θΔt) = e^(-{theta:.6f} × {dt}) = {exp_neg_theta_dt:.6f}")
    print(f"  e^(-2θΔt) = e^(-{2*theta:.6f} × {dt}) = {exp_neg_2theta_dt:.6f}")
    
    n = len(data) - 1
    sum_squared = 0.0
    for i in range(n):
        diff = data[i+1] - data[i] - mu * (1 - exp_neg_theta_dt)
        sum_squared += diff ** 2
    
    denominator = n * (1 - exp_neg_2theta_dt)
    sigma_squared = (2 * theta * sum_squared) / denominator
    
    print(f"  Σ squared differences: {sum_squared:.6f}")
    print(f"  Denominator: {denominator:.6f}")
    print(f"  σ² = (2 × {theta:.6f} × {sum_squared:.6f}) / {denominator:.6f} = {sigma_squared:.6f}")
    print(f"Estimated Sigma (σ): {sigma:.6f}")
    
    if true_params:
        sigma_error = abs(sigma - true_params['sigma']) / true_params['sigma'] * 100
        print(f"True Sigma: {true_params['sigma']:.6f}")
        print(f"Estimation Error: {sigma_error:.2f}%")
    
    print("\n5. STATIONARY DISTRIBUTION PROPERTIES")
    print("-"*70)
    stationary_var = (sigma ** 2) / (2 * theta)
    stationary_std = np.sqrt(stationary_var)
    print(f"Stationary Variance: σ² / (2θ) = {sigma**2:.6f} / (2 × {theta:.6f}) = {stationary_var:.6f}")
    print(f"Stationary Standard Deviation: {stationary_std:.6f}")
    print(f"Interpretation: Long-term variance around mean is {stationary_std:.4f}")
    
    print("\n6. PARAMETER ESTIMATION SUMMARY")
    print("-"*70)
    print(f"{'Parameter':<12} {'Estimated':<15} {'True Value':<15} {'Error %':<10}")
    print("-"*70)
    
    if true_params:
        params = [
            ('θ (theta)', theta, true_params.get('theta')),
            ('μ (mu)', mu, true_params.get('mu')),
            ('σ (sigma)', sigma, true_params.get('sigma'))
        ]
        
        for name, est, true in params:
            if true is not None:
                error = abs(est - true) / abs(true) * 100
                print(f"{name:<12} {est:<15.6f} {true:<15.6f} {error:<10.2f}%")
            else:
                print(f"{name:<12} {est:<15.6f} {'N/A':<15} {'N/A':<10}")
    else:
        print(f"{'θ (theta)':<12} {theta:<15.6f}")
        print(f"{'μ (mu)':<12} {mu:<15.6f}")
        print(f"{'σ (sigma)':<12} {sigma:<15.6f}")
    
    print("="*70)
    
    return {
        'theta': theta,
        'mu': mu,
        'sigma': sigma,
        'rho': rho,
        'half_life': half_life,
        'stationary_variance': stationary_var,
        'stationary_std': stationary_std
    }


def compare_estimation_methods_detailed(data, dt=1.0, true_params=None):
    estimator = OUEstimator()
    
    print("\n" + "="*70)
    print("ESTIMATION METHOD COMPARISON")
    print("="*70)
    
    methods = {
        'MLE': estimator.estimate_mle,
        'Regression': estimator.estimate_regression,
        'OLS': estimator.estimate_ols
    }
    
    results = {}
    for method_name, method_func in methods.items():
        print(f"\n{method_name} Method:")
        print("-"*70)
        theta, mu, sigma = method_func(data, dt)
        
        results[method_name] = {
            'theta': theta,
            'mu': mu,
            'sigma': sigma,
            'half_life': estimator.half_life(),
            'stationary_variance': estimator.stationary_variance()
        }
        
        print(f"  θ = {theta:.6f}")
        print(f"  μ = {mu:.6f}")
        print(f"  σ = {sigma:.6f}")
        if results[method_name]['half_life']:
            print(f"  Half-life = {results[method_name]['half_life']:.4f}")
        
        if true_params:
            theta_err = abs(theta - true_params['theta']) / true_params['theta'] * 100
            mu_err = abs(mu - true_params['mu']) / abs(true_params['mu']) * 100
            sigma_err = abs(sigma - true_params['sigma']) / true_params['sigma'] * 100
            print(f"  Error: θ={theta_err:.2f}%, μ={mu_err:.2f}%, σ={sigma_err:.2f}%")
    
    print("\n" + "="*70)
    print("METHOD COMPARISON SUMMARY")
    print("="*70)
    print(f"{'Method':<12} {'θ':<12} {'μ':<12} {'σ':<12} {'Half-life':<12}")
    print("-"*70)
    
    for method_name, result in results.items():
        print(f"{method_name:<12} {result['theta']:<12.6f} {result['mu']:<12.6f} "
              f"{result['sigma']:<12.6f} {result['half_life'] or 0:<12.4f}")
    
    if true_params:
        print("\nTrue Values:")
        print(f"  θ = {true_params['theta']:.6f}")
        print(f"  μ = {true_params['mu']:.6f}")
        print(f"  σ = {true_params['sigma']:.6f}")
    
    return results


# Note: This module provides analysis functions for real data
# Use detailed_parameter_analysis() and compare_estimation_methods_detailed()
# with your real market data from test_real_data.py

