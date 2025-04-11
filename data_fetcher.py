import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
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
        # For Yahoo Finance, use "=X" suffix for currency pairs
        ticker = f"{pair}=X"
        
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
                raise Exception(f"No data returned for {pair}")
                
        except Exception as e:
            st.warning(f"Error fetching data for {pair}: {str(e)}")
            continue
    
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
                raise Exception(f"No data returned for {ticker}")
                
        except Exception as e:
            st.warning(f"Error fetching data for {ticker}: {str(e)}")
            continue
    
    return all_data
