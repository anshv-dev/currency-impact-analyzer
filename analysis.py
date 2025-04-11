import pandas as pd
import numpy as np
from scipy import stats

def calculate_percentage_changes(price_data):
    """
    Calculate daily percentage changes for price data
    
    Args:
        price_data: DataFrame of price data
        
    Returns:
        DataFrame of percentage changes
    """
    if price_data is None or price_data.empty:
        return pd.DataFrame()
    
    # Calculate percent change
    pct_change = price_data.pct_change() * 100
    
    # Drop the first row (NaN values)
    pct_change = pct_change.dropna()
    
    return pct_change

def calculate_correlation(series1, series2):
    """
    Calculate Pearson correlation coefficient and p-value 
    between two time series
    
    Args:
        series1: First time series (pandas Series)
        series2: Second time series (pandas Series)
        
    Returns:
        Tuple of (correlation coefficient, p-value)
    """
    # Align the series to make sure dates match
    s1, s2 = series1.align(series2, join='inner')
    
    # Remove any NaN values
    mask = ~(np.isnan(s1) | np.isnan(s2))
    s1 = s1[mask]
    s2 = s2[mask]
    
    # Calculate correlation if we have enough data points
    if len(s1) > 1:
        correlation, p_value = stats.pearsonr(s1, s2)
        return correlation, p_value
    else:
        return np.nan, np.nan

def get_correlation_label(correlation):
    """
    Get a human-readable label and color for a correlation value
    
    Args:
        correlation: Correlation coefficient
        
    Returns:
        Tuple of (label, color)
    """
    if np.isnan(correlation):
        return "Insufficient data", "gray"
    
    abs_corr = abs(correlation)
    
    if abs_corr >= 0.7:
        strength = "Strong"
        color = "green" if correlation > 0 else "red"
    elif abs_corr >= 0.3:
        strength = "Moderate"
        color = "blue" if correlation > 0 else "orange"
    else:
        strength = "Weak"
        color = "gray"
    
    direction = "Positive" if correlation > 0 else "Negative"
    
    return f"{strength} {direction}", color

def calculate_summary_statistics(data):
    """
    Calculate summary statistics for price data
    
    Args:
        data: DataFrame of price data
        
    Returns:
        DataFrame of summary statistics
    """
    # Calculate basic statistics
    stats = pd.DataFrame({
        'Min': data.min(),
        'Max': data.max(),
        'Mean': data.mean(),
        'Median': data.median(),
        'Std Dev': data.std(),
        'Volatility (%)': data.pct_change().std() * 100 * np.sqrt(252)  # Annualized volatility
    })
    
    return stats.transpose()
