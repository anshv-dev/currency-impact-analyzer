import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import streamlit as st

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_exchange_rates(currency_pairs, start_date, end_date):
    """
    Fetch exchange rate data for specified currency pairs
    
    Args:
        currency_pairs: List of currency pair codes (e.g., 'USD-INR')
        start_date: Start date for data
        end_date: End date for data
        
    Returns:
        Pandas DataFrame with exchange rate data
    """
    # Convert dates to string format for yfinance
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')  # Add a day to include end_date
    
    all_data = pd.DataFrame()
    
    for pair in currency_pairs:
        # Convert format from "USD-INR" to "USDINR=X" for Yahoo Finance
        # Make sure pair is a string before calling replace on it
        pair_str = str(pair)
        ticker = f"{pair_str.replace('-', '')}=X"
        
        try:
            # Fetch data using yfinance
            data = yf.download(
                ticker,
                start=start_date_str,
                end=end_date_str,
                progress=False
            )
            
            # Select closing prices and rename column
            if not data.empty:
                pair_data = data['Close'].rename(pair)
                
                # If all_data is empty, initialize it with the index
                if all_data.empty:
                    all_data = pd.DataFrame(index=data.index)
                
                # Add the current pair data
                all_data[pair] = pair_data
            else:
                st.warning(f"No data returned for {pair}. Using generated sample data.")
                # Generate sample data if actual data is not available
                if all_data.empty:
                    # Create date range from start_date to end_date
                    date_range = pd.date_range(start=start_date, end=end_date)
                    all_data = pd.DataFrame(index=date_range)
                
                # Generate realistic sample data based on currency pair
                base_value = 0
                if "USD-INR" in pair:
                    base_value = 83.0  # Approximate USD-INR exchange rate
                elif "EUR-INR" in pair:
                    base_value = 90.0  # Approximate EUR-INR exchange rate
                elif "JPY-INR" in pair:
                    base_value = 0.55  # Approximate JPY-INR exchange rate (for 1 JPY)
                elif "CHF-INR" in pair:
                    base_value = 93.0  # Approximate CHF-INR exchange rate
                else:
                    base_value = 75.0  # Default value
                
                # Create slightly varying exchange rate data
                np.random.seed(42)  # For reproducibility
                volatility = 0.02  # 2% volatility
                
                # Generate random walk starting from base_value
                num_days = len(all_data.index)
                daily_returns = np.random.normal(0, volatility, num_days)
                
                # Cumulative returns
                cumulative_returns = np.exp(np.cumsum(daily_returns)) 
                
                # Scale by base value and add some trend
                values = base_value * cumulative_returns * (1 + np.linspace(0, 0.05, num_days))
                
                all_data[pair] = values
                
        except Exception as e:
            st.warning(f"Error fetching data for {pair}: {str(e)}")
            # Generate sample data here too if there's an exception
            if all_data.empty:
                date_range = pd.date_range(start=start_date, end=end_date)
                all_data = pd.DataFrame(index=date_range)
            
            # Base values similar to above
            base_value = 80.0
            if "USD-INR" in pair:
                base_value = 83.0
            elif "EUR-INR" in pair:
                base_value = 90.0
            elif "JPY-INR" in pair:
                base_value = 0.55
            elif "CHF-INR" in pair:
                base_value = 93.0
            
            # Create data with different seed
            np.random.seed(hash(pair) % 100)  # Different seed for each pair
            volatility = 0.015
            num_days = len(all_data.index)
            daily_returns = np.random.normal(0, volatility, num_days)
            cumulative_returns = np.exp(np.cumsum(daily_returns))
            values = base_value * cumulative_returns * (1 + np.linspace(0, 0.03, num_days))
            
            all_data[pair] = values
    
    return all_data

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_prices(stock_tickers, start_date, end_date):
    """
    Fetch stock price data for specified tickers
    
    Args:
        stock_tickers: List of stock ticker symbols
        start_date: Start date for data
        end_date: End date for data
        
    Returns:
        Pandas DataFrame with stock price data
    """
    # Convert dates to string format for yfinance
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')  # Add a day to include end_date
    
    all_data = pd.DataFrame()
    
    for ticker in stock_tickers:
        try:
            # Fetch data using yfinance
            data = yf.download(
                ticker,
                start=start_date_str,
                end=end_date_str,
                progress=False
            )
            
            # Select closing prices and rename column
            if not data.empty:
                stock_data = data['Close'].rename(ticker)
                
                # If all_data is empty, initialize it with the index
                if all_data.empty:
                    all_data = pd.DataFrame(index=data.index)
                
                # Add the current stock data
                all_data[ticker] = stock_data
            else:
                st.warning(f"No data returned for {ticker}. Using generated sample data.")
                # Generate sample data if actual data is not available
                if all_data.empty:
                    # Create date range from start_date to end_date
                    date_range = pd.date_range(start=start_date, end=end_date)
                    all_data = pd.DataFrame(index=date_range)
                
                # Generate realistic sample data based on stock ticker
                # Set base values for common Indian IT companies
                base_value = 1000.0  # Default
                if "TCS.NS" in ticker:
                    base_value = 3500.0  # TCS
                elif "INFY.NS" in ticker:
                    base_value = 1500.0  # Infosys
                elif "WIPRO.NS" in ticker:
                    base_value = 400.0  # Wipro
                elif "HCLTECH.NS" in ticker:
                    base_value = 1100.0  # HCL
                elif "TECHM.NS" in ticker:
                    base_value = 1200.0  # Tech Mahindra
                elif "LTTS.NS" in ticker:
                    base_value = 3800.0  # L&T Technology
                elif "MINDTREE.NS" in ticker:
                    base_value = 3000.0  # Mindtree
                elif "MPHASIS.NS" in ticker:
                    base_value = 2200.0  # Mphasis
                
                # Create slightly varying stock price data
                np.random.seed(hash(ticker) % 100)  # Different seed for each stock
                volatility = 0.03  # Higher volatility for stocks vs currencies
                
                # Generate random walk
                num_days = len(all_data.index)
                daily_returns = np.random.normal(0.0005, volatility, num_days)  # Slight upward bias
                
                # Cumulative returns
                cumulative_returns = np.exp(np.cumsum(daily_returns))
                
                # Scale by base value and add some trend
                values = base_value * cumulative_returns
                
                all_data[ticker] = values
                
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {str(e)}")
            # Generate sample data here too if there's an exception
            if all_data.empty:
                date_range = pd.date_range(start=start_date, end=end_date)
                all_data = pd.DataFrame(index=date_range)
            
            # Base values for IT companies (same as above)
            base_value = 1000.0
            if "TCS.NS" in ticker:
                base_value = 3500.0
            elif "INFY.NS" in ticker:
                base_value = 1500.0
            elif "WIPRO.NS" in ticker:
                base_value = 400.0
            elif "HCLTECH.NS" in ticker:
                base_value = 1100.0
            elif "TECHM.NS" in ticker:
                base_value = 1200.0
            elif "LTTS.NS" in ticker:
                base_value = 3800.0
            elif "MINDTREE.NS" in ticker:
                base_value = 3000.0
            elif "MPHASIS.NS" in ticker:
                base_value = 2200.0
            
            # Different seed than above
            np.random.seed((hash(ticker) + 1) % 100)
            volatility = 0.025
            num_days = len(all_data.index)
            # Slight downward bias for error case (for variety)
            daily_returns = np.random.normal(-0.0001, volatility, num_days)
            cumulative_returns = np.exp(np.cumsum(daily_returns))
            values = base_value * cumulative_returns
            
            all_data[ticker] = values
    
    return all_data
