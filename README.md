# Currency Impact Analyzer for IT Companies

A Streamlit-based financial analysis tool that tracks currency exchange rates and their correlation with IT company stock performance.

## Overview

This application analyzes the impact of currency exchange rates on Indian IT companies' stock performance. It helps investors and analysts understand how currency fluctuations affect company valuations.

The tool tracks daily exchange rates (USD/INR, EUR/INR, JPY/INR, CHF/INR) and compares them against stock performance of leading Indian IT companies.

## Features

- **Exchange Rate Tracking**: Monitor daily currency rates for multiple currency pairs against the Indian Rupee
- **Stock Price Analysis**: Track stock prices for major Indian IT companies
- **Correlation Analysis**: Visualize and analyze correlations between currency movements and stock performance
- **Alert System**: Set thresholds for significant currency movements
- **Data Visualization**: Interactive charts and graphs for easy data interpretation

## Setup and Usage

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:5000)

## Data Sources

The application attempts to fetch real-time data from Yahoo Finance. If live data cannot be retrieved, the application will use generated sample data based on realistic currency rates and stock prices to demonstrate functionality.

## Dependencies

- Python 3.6+
- Streamlit
- Pandas
- NumPy
- Plotly
- yfinance
- statsmodels

## Structure

- `app.py`: Main Streamlit application
- `data_fetcher.py`: Handles data retrieval from Yahoo Finance
- `analysis.py`: Functions for correlation and percentage change calculations
- `alert_system.py`: Alert system for currency movements