import streamlit as st
import yfinance as yf
import pandas as pd

# Define tickers and their respective coordinates (latitude and longitude)
data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom'],
    'Index': ['^GSPC', '000001.SS', '^N225', '^GDAXI', '^FTSE'],
    'Latitude': [37.7749, 39.9042, 35.6762, 51.1657, 51.509865],
    'Longitude': [-122.4194, 116.4074, 139.6503, 10.4515, -0.118092],
    'Value': [None] * 5  # Placeholder for index values
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to fetch stock index values
def fetch_index_values(tickers):
    for i, ticker in enumerate(tickers):
        try:
            ticker_data = yf.Ticker(ticker).history(period="1d")
            current_value = ticker_data['Close'][-1]
            df.at[i, 'Value'] = current_value
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

# Fetch stock index values
fetch_index_values(df['Index'])

# Display DataFrame with fetched values
st.write(df)

# Plot map
st.map(df[['Latitude', 'Longitude']])
