import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io
import base64

# Import custom modules
from data_fetcher import get_exchange_rates, get_stock_prices
from analysis import calculate_percentage_changes, calculate_correlation, get_correlation_label
from alert_system import check_alerts, setup_alert

# Page configuration
st.set_page_config(
    page_title="Currency Impact Analyzer for IT Companies",
    page_icon="📈",
    layout="wide",
)

# App title and description
st.title("Currency Impact Analyzer for IT Companies")
st.markdown("""
This tool analyzes the impact of currency exchange rates on Indian IT companies' stock performance.
It helps investors and analysts understand how currency fluctuations affect company valuations.
""")

# Sidebar for inputs
st.sidebar.header("Analysis Parameters")

# Date range selection
st.sidebar.subheader("Select Date Range")
today = datetime.now().date()
default_start_date = today - timedelta(days=90)  # Default to 90 days of data
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", today)

if start_date > end_date:
    st.error("Error: Start date cannot be after end date.")
    st.stop()

# Currency selection
st.sidebar.subheader("Select Currencies")
currencies = {
    "USD/INR": "USD-INR",
    "EUR/INR": "EUR-INR",
    "JPY/INR": "JPY-INR",
    "CHF/INR": "CHF-INR"
}
selected_currencies = st.sidebar.multiselect(
    "Currencies to analyze",
    list(currencies.keys()),
    default=["USD/INR", "EUR/INR"]
)

# IT Companies selection
st.sidebar.subheader("Select IT Companies")
companies = {
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Tech Mahindra": "TECHM.NS",
    "L&T Technology Services": "LTTS.NS",
    "Mindtree": "MINDTREE.NS",
    "Mphasis": "MPHASIS.NS"
}
selected_companies = st.sidebar.multiselect(
    "Companies to analyze",
    list(companies.keys()),
    default=["Tata Consultancy Services", "Infosys", "Wipro"]
)

# Alert system setup in sidebar
st.sidebar.subheader("Alert System")
alert_active = st.sidebar.checkbox("Enable Currency Movement Alerts")
alert_threshold = 0.0

if alert_active:
    alert_threshold = st.sidebar.slider(
        "Alert Threshold (%)",
        min_value=0.5,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Send alert when daily currency change exceeds this percentage"
    )
    alert_email = st.sidebar.text_input("Email for alerts (optional)")

# Sidebar message about data sources
st.sidebar.markdown("""
---
**Note on Data Sources**

The application attempts to fetch real-time data from Yahoo Finance. 
If live data cannot be retrieved, the application will use generated sample data 
based on realistic currency rates and stock prices to demonstrate functionality.
""")

# Load data based on selections
with st.spinner("Fetching exchange rate data..."):
    try:
        currency_data = get_exchange_rates(
            [currencies[c] for c in selected_currencies],
            start_date,
            end_date
        )
        
        if currency_data is None or currency_data.empty:
            st.error("Failed to fetch currency data. Please check your selections and try again.")
            st.stop()
        
        # Check if we have at least some data for currencies
        data_source = "Real-time data from Yahoo Finance"
        for currency in selected_currencies:
            currency_code = currencies[currency]
            if currency_code not in currency_data.columns:
                data_source = "Simulated data (live data unavailable)"
                break
            
    except Exception as e:
        st.error(f"Error fetching currency data: {str(e)}")
        st.stop()

with st.spinner("Fetching stock price data..."):
    try:
        stock_data = get_stock_prices(
            [companies[c] for c in selected_companies],
            start_date,
            end_date
        )
        
        if stock_data is None or stock_data.empty:
            st.error("Failed to fetch stock data. Please check your selections and try again.")
            st.stop()
        
        # Check if we have real data for stocks
        for company in selected_companies:
            company_code = companies[company]
            if company_code not in stock_data.columns:
                data_source = "Simulated data (live data unavailable)"
                break
            
    except Exception as e:
        st.error(f"Error fetching stock data: {str(e)}")
        st.stop()

# Inform user about the data source being used
if data_source == "Simulated data (live data unavailable)":
    st.info("""
    ℹ️ Note: Some required data couldn't be retrieved from Yahoo Finance. 
    The application is using simulated data to demonstrate functionality. 
    The patterns and trends shown are for illustration purposes only.
    """)

# Calculate percentage changes for analysis
with st.spinner("Calculating percentage changes..."):
    currency_pct_change = calculate_percentage_changes(currency_data)
    stock_pct_change = calculate_percentage_changes(stock_data)

# Main dashboard
st.header("Currency Exchange Rates Overview")
tab1, tab2, tab3, tab4 = st.tabs(["Exchange Rates", "IT Stocks", "Correlation Analysis", "Alerts"])

with tab1:
    st.subheader("Exchange Rate Trends")
    
    # Daily exchange rates chart
    fig_rates = px.line(
        currency_data,
        x=currency_data.index,
        y=currency_data.columns,
        title="Daily Exchange Rates",
        labels={"value": "Exchange Rate", "variable": "Currency Pair", "date": "Date"}
    )
    fig_rates.update_layout(height=500)
    st.plotly_chart(fig_rates, use_container_width=True)
    
    # Daily percentage changes
    st.subheader("Daily Exchange Rate % Changes")
    fig_pct = px.line(
        currency_pct_change,
        x=currency_pct_change.index,
        y=currency_pct_change.columns,
        title="Daily Exchange Rate % Changes",
        labels={"value": "% Change", "variable": "Currency Pair", "date": "Date"}
    )
    fig_pct.update_layout(height=500)
    st.plotly_chart(fig_pct, use_container_width=True)
    
    # Display raw data
    with st.expander("View Raw Exchange Rate Data"):
        st.dataframe(currency_data)
        
        # Download button for raw data
        csv = currency_data.to_csv()
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="exchange_rates.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

with tab2:
    st.subheader("IT Company Stock Performance")
    
    # Stock prices chart
    fig_stocks = px.line(
        stock_data,
        x=stock_data.index,
        y=stock_data.columns,
        title="IT Company Stock Prices",
        labels={"value": "Stock Price (INR)", "variable": "Company", "date": "Date"}
    )
    fig_stocks.update_layout(height=500)
    st.plotly_chart(fig_stocks, use_container_width=True)
    
    # Daily percentage changes
    st.subheader("Daily Stock Price % Changes")
    fig_stock_pct = px.line(
        stock_pct_change,
        x=stock_pct_change.index,
        y=stock_pct_change.columns,
        title="Daily Stock Price % Changes",
        labels={"value": "% Change", "variable": "Company", "date": "Date"}
    )
    fig_stock_pct.update_layout(height=500)
    st.plotly_chart(fig_stock_pct, use_container_width=True)
    
    # Display raw data
    with st.expander("View Raw Stock Price Data"):
        st.dataframe(stock_data)
        
        # Download button for raw data
        csv = stock_data.to_csv()
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="stock_prices.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

with tab3:
    st.subheader("Correlation Analysis")
    
    # Currency selection for correlation
    if len(selected_currencies) > 0 and len(selected_companies) > 0:
        corr_currency = st.selectbox("Select Currency", selected_currencies)
        corr_currency_code = currencies[corr_currency]
        
        st.write("### Correlation between Currency and Stock Performance")
        
        # Create correlation heatmap
        corr_data = pd.DataFrame()
        corr_data[corr_currency] = currency_pct_change[corr_currency_code]
        
        for company in selected_companies:
            company_code = companies[company]
            corr_data[company] = stock_pct_change[company_code]
        
        correlation_matrix = corr_data.corr()
        
        # Display correlation matrix
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            labels=dict(color="Correlation"),
            title=f"Correlation Matrix: {corr_currency} vs IT Stocks"
        )
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Detailed correlation analysis
        st.write("### Detailed Correlation Analysis")
        
        for company in selected_companies:
            company_code = companies[company]
            correlation, p_value = calculate_correlation(
                currency_pct_change[corr_currency_code],
                stock_pct_change[company_code]
            )
            
            corr_label, corr_color = get_correlation_label(correlation)
            
            st.markdown(
                f"**{company}** vs **{corr_currency}**: "
                f"Correlation = {correlation:.4f} "
                f"(<span style='color:{corr_color}'>{corr_label}</span>), "
                f"P-value = {p_value:.4f}",
                unsafe_allow_html=True
            )
            
            # Scatter plot
            fig_scatter = px.scatter(
                x=currency_pct_change[corr_currency_code],
                y=stock_pct_change[company_code],
                trendline="ols",
                labels={
                    "x": f"{corr_currency} Daily % Change",
                    "y": f"{company} Daily % Change"
                },
                title=f"{company} vs {corr_currency} Correlation"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Please select at least one currency and one company to perform correlation analysis.")

with tab4:
    st.subheader("Currency Movement Alerts")
    
    if alert_active:
        setup_info = setup_alert(alert_threshold, alert_email)
        st.info(f"Alert system is active. You will be notified when daily currency movements exceed {alert_threshold}%.")
        
        # Check for alerts based on recent data
        alerts = check_alerts(currency_pct_change, alert_threshold)
        
        if alerts:
            st.warning("The following alerts were detected based on recent data:")
            for alert in alerts:
                st.markdown(f"* **{alert['currency']}**: {alert['change']:.2f}% change on {alert['date']}")
        else:
            st.success("No currency movements above the threshold in the selected period.")
            
    else:
        st.write("The alert system is currently disabled. Enable it in the sidebar to receive notifications about significant currency movements.")

    # Alert history visualization (if we had persistent storage)
    st.write("### Recent Currency Movements")
    
    # Get max absolute percentage change for each currency
    max_changes = currency_pct_change.abs().max()
    
    # Create a bar chart of maximum movements
    fig_max = px.bar(
        x=max_changes.index,
        y=max_changes.values,
        labels={"x": "Currency", "y": "Maximum Daily % Change (Absolute)"},
        title="Maximum Daily Currency Movements in Selected Period"
    )
    
    # Add threshold line
    if alert_active:
        fig_max.add_hline(
            y=alert_threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Alert Threshold ({alert_threshold}%)"
        )
    
    st.plotly_chart(fig_max, use_container_width=True)

# Execution Info
st.markdown("---")
st.caption(f"Data time range: {start_date} to {end_date}")
st.caption(f"Data source: {data_source}")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
