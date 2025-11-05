"""
Ornstein-Uhlenbeck Process Model
By Josephina Kim (JK)

This simulates the OU process - the core mean-reverting stochastic model.
Uses exact solution for accurate simulation.
"""

import numpy as np
from scipy import stats
from ou_estimator import OUEstimator


class OUProcess:
    def __init__(self, theta, mu, sigma, dt=1.0):
        self.theta = theta
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.x0 = None
    
    def simulate(self, n_steps, x0=None, seed=None):
        if seed is not None:
            np.random.seed(seed)
        
        if x0 is None:
            x0 = self.mu
        self.x0 = x0
        
        path = np.zeros(n_steps)
        path[0] = x0
        
        sqrt_dt = np.sqrt(self.dt)
        
        for i in range(1, n_steps):
            drift = self.theta * (self.mu - path[i-1]) * self.dt
            diffusion = self.sigma * np.random.normal(0, 1) * sqrt_dt
            path[i] = path[i-1] + drift + diffusion
        
        return path
    
    def simulate_exact(self, n_steps, x0=None, seed=None):
        if seed is not None:
            np.random.seed(seed)
        
        if x0 is None:
            x0 = self.mu
        self.x0 = x0
        
        path = np.zeros(n_steps)
        path[0] = x0
        
        exp_neg_theta_dt = np.exp(-self.theta * self.dt)
        variance = (self.sigma ** 2) * (1 - np.exp(-2 * self.theta * self.dt)) / (2 * self.theta)
        std_dev = np.sqrt(max(variance, 0.001))
        
        for i in range(1, n_steps):
            path[i] = self.mu + (path[i-1] - self.mu) * exp_neg_theta_dt + \
                      np.random.normal(0, std_dev)
        
        return path
    
    def expected_value(self, t, x0=None):
        if x0 is None:
            x0 = self.mu if self.x0 is None else self.x0
        return self.mu + (x0 - self.mu) * np.exp(-self.theta * t)
    
    def variance(self, t):
        return (self.sigma ** 2) * (1 - np.exp(-2 * self.theta * t)) / (2 * self.theta)
    
    def probability_reversion(self, current_value, threshold=None):
        if threshold is None:
            threshold = self.mu
        
        deviation = current_value - self.mu
        if abs(deviation) < 1e-10:
            return 0.5
        
        expected_time = self.expected_time_to_mean(current_value)
        if expected_time is None:
            return 0.5
        
        z_score = deviation / np.sqrt(self.stationary_variance())
        return 1 - abs(stats.norm.cdf(z_score) - 0.5) * 2
    
    def expected_time_to_mean(self, current_value):
        if self.theta <= 0:
            return None
        deviation = abs(current_value - self.mu)
        if deviation < 1e-10:
            return 0.0
        return -np.log(deviation / (self.mu + 1e-10)) / self.theta
    
    def stationary_variance(self):
        if self.theta <= 0:
            return None
        return (self.sigma ** 2) / (2 * self.theta)
    
    def half_life(self):
        return np.log(2) / self.theta
    
    def get_parameters(self):
        return {
            'theta': self.theta,
            'mu': self.mu,
            'sigma': self.sigma,
            'dt': self.dt
        }

