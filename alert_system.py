import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st

def setup_alert(threshold, email=None):
    """
    Setup alert system for currency movements
    
    Args:
        threshold: Percentage threshold for alerts
        email: Email address to send alerts to (optional)
        
    Returns:
        Dictionary with alert configuration
    """
    alert_config = {
        'threshold': threshold,
        'email': email,
        'setup_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return alert_config

def check_alerts(currency_data, threshold):
    """
    Check for currency movements exceeding the threshold
    
    Args:
        currency_data: DataFrame of currency percentage changes
        threshold: Percentage threshold for alerts
        
    Returns:
        List of alert dictionaries
    """
    if currency_data is None or currency_data.empty:
        return []
    
    alerts = []
    
    # Check each currency in the data
    for currency in currency_data.columns:
        # Find dates where the absolute percentage change exceeds the threshold
        alert_dates = currency_data.index[np.abs(currency_data[currency]) > threshold]
        
        for date in alert_dates:
            change = currency_data.loc[date, currency]
            alerts.append({
                'currency': currency,
                'date': date.strftime('%Y-%m-%d'),
                'change': change,
                'direction': 'increase' if change > 0 else 'decrease'
            })
    
    # Sort alerts by date (most recent first)
    alerts.sort(key=lambda x: x['date'], reverse=True)
    
    return alerts

def send_email_alert(alert_data, recipient_email):
    """
    Send email alert for significant currency movements
    
    Args:
        alert_data: Dictionary with alert information
        recipient_email: Email address to send alert to
        
    Returns:
        Boolean indicating success or failure
    """
    # Skip if no email is provided
    if not recipient_email:
        return False
    
    # Get email credentials from environment variables
    smtp_server = os.getenv('SMTP_SERVER', '')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    # Skip if no credentials are provided
    if not all([smtp_server, smtp_port, smtp_username, smtp_password]):
        st.warning("Email alerts are disabled due to missing SMTP configuration.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = recipient_email
        msg['Subject'] = f"Currency Alert: {alert_data['currency']} {alert_data['direction']} by {abs(alert_data['change']):.2f}%"
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Currency Movement Alert</h2>
            <p>This is an automated alert from the Currency Impact Analyzer.</p>
            <p><strong>{alert_data['currency']}</strong> has {alert_data['direction']}d by {abs(alert_data['change']):.2f}% on {alert_data['date']}.</p>
            <p>This movement exceeds your configured threshold of {alert_data['threshold']}%.</p>
            <hr>
            <p>To adjust your alert settings, please visit the application.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        return True
    
    except Exception as e:
        st.error(f"Failed to send email alert: {str(e)}")
        return False
