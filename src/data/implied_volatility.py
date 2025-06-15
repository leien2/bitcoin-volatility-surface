import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price
    
    Parameters:
    S: Underlying asset price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free interest rate
    sigma: Volatility
    option_type: Option type ('call' or 'put')
    
    Returns:
    Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return price

def calculate_implied_volatility(option_price, S, K, T, r, option_type='call', 
                              initial_vol=0.3, precision=0.00001, max_iterations=100):
    """
    Calculate implied volatility using Newton-Raphson method
    
    Parameters:
    option_price: Actual option price
    S: Underlying asset price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free interest rate
    option_type: Option type ('call' or 'put')
    initial_vol: Initial volatility guess
    precision: Required precision
    max_iterations: Maximum number of iterations
    
    Returns:
    Implied volatility
    """
    sigma = initial_vol
    
    for i in range(max_iterations):
        # Calculate option price
        price = black_scholes(S, K, T, r, sigma, option_type)
        
        # Calculate derivative of option price with respect to volatility (vega)
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        vega = S * np.sqrt(T) * norm.pdf(d1)
        
        # Price difference
        diff = price - option_price
        
        # Check if required precision is reached
        if abs(diff) < precision:
            return sigma
        
        # Prevent division issues when vega is too small
        if abs(vega) < 1e-8:
            return sigma
            
        # Update volatility (Newton-Raphson method)
        sigma = sigma - diff / vega
        
        # Prevent volatility from becoming negative or too small
        if sigma <= 0.001:
            sigma = 0.001
    
    return sigma