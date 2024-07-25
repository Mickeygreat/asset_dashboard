import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Define the data
data = {
    'Country': [
        'United States', 'China', 'Japan', 'Germany', 'United Kingdom',
        'United Kingdom', 'United States', 'United States', 'United Kingdom',
        'Germany', 'France', 'Europe', 'Europe', 'Belgium', 'Russia', 
        'Japan', 'Hong Kong', 'China', 'China', 'Singapore', 'Australia', 
        'Australia', 'India', 'Indonesia', 'Malaysia', 'New Zealand', 
        'South Korea', 'Taiwan', 'Canada', 'Brazil', 'Mexico', 'Chile', 
        'Argentina', 'Israel', 'Egypt', 'South Africa'
    ],
    'Index': [
        '^GSPC', '000001.SS', '^N225', '^GDAXI', '^FTSE',
        '^BUK100P', '^RUT', '^VIX', '^FTSE', '^GDAXI', 
        '^FCHI', '^STOXX50E', '^N100', '^BFX', 'IMOEX.ME', 
        '^N225', '^HSI', '000001.SS', '399001.SZ', '^STI', 
        '^AXJO', '^AORD', '^BSESN', '^JKSE', '^KLSE', 
        '^NZ50', '^KS11', '^TWII', '^GSPTSE', '^BVSP', 
        '^MXX', '^IPSA', '^MERV', '^TA125.TA', '^CASE30', 
        '^JN0U.JO'
    ],
    'Currency': [
        'USD', 'CNY', 'JPY', 'EUR', 'GBP',
        'GBP', 'USD', 'USD', 'GBP', 'EUR', 
        'EUR', 'EUR', 'EUR', 'EUR', 'RUB', 
        'JPY', 'HKD', 'CNY', 'CNY', 'SGD', 
        'AUD', 'AUD', 'INR', 'IDR', 'MYR', 
        'NZD', 'KRW', 'TWD', 'CAD', 'BRL', 
        'MXN', 'CLP', 'ARS', 'ILS', 'EGP', 
        'USD'
    ],
    'Latitude': [
        37.7749, 39.9042, 35.6762, 51.1657, 51.509865,
        51.509865, 37.7749, 37.7749, 51.509865, 51.1657, 
        51.1657, 48.8566, 48.8566, 50.8503, 55.7558, 
        35.6762, 22.3193, 31.2304, 22.3193, 1.3521, 
        -35.2809, -35.2809, 19.0760, -6.2088, 3.139, 
        -41.2865, 37.5665, 25.0375, 45.4215, -23.5505, 
        19.4326, -33.9249
    ],
    'Longitude': [
        -122.4194, 116.4074, 139.6503, 10.4515, -0.118092,
        -0.118092, -122.4194, -122.4194, -0.118092, 10.4515, 
        10.4515, 2.3522, 2.3522, 4.3517, 37.6173, 
        139.6503, 114.1694, 121.4737, 114.1694, 103.8198, 
        149.1244, 149.1244, 72.8777, 106.8456, 101.6869, 
        174.7762, 126.9780, 121.5654, -79.3832, -46.6333, 
        -99.1332, -70.6483, 34.7968, 28.9794
    ],
    'Value': [None] * 36  # Placeholder for index values
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to fetch stock index values
def fetch_index_values(tickers):
    for i, ticker in enumerate(tickers):
        try:
            ticker_data = yf.Ticker(ticker).history(period="1d")
            current_value = ticker_data['Close'].iloc[-1]
            df.at[i, 'Value'] = f"{current_value:.2f}"
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

# Fetch stock index values
fetch_index_values(df['Index'])

# Plot map using Plotly
st.title("Interactive Globe View of Stock Exchanges")

fig = go.Figure()

# Add scattergeo trace for the globe view
fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df['Country'] + '<br>Index: ' + df['Index'] + '<br>Value: ' + df['Value'].astype(str),
    mode='markers+text',
    marker=dict(size=10, color='blue', opacity=0.8),
    textposition='top center'
))

# Set globe projection and layout settings
fig.update_geos(
    projection_type="orthographic",
    showland=True,
    landcolor="rgb(242, 242, 242)",
    showocean=True,
    oceancolor="rgb(204, 204, 255)",
    showcoastlines=True,
    coastlinecolor="rgb(102, 102, 102)",
    showlakes=True,
    lakecolor="rgb(255, 255, 255)",
    showcountries=True,
    countrycolor="rgb(204, 204, 204)"
)

fig.update_layout(
    title="Stock Exchanges Around the Globe",
    geo=dict(
        showland=True,
        landcolor="rgb(242, 242, 242)",
        showocean=True,
        oceancolor="rgb(204, 204, 255)",
        showcoastlines=True,
        coastlinecolor="rgb(102, 102, 102)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
        showcountries=True,
        countrycolor="rgb(204, 204, 204)"
    ),
    height=800,  # Adjust height as needed
    margin={"r":0,"t":0,"l":0,"b":0}  # Remove margins to make the map full-screen
)

# Display map
st.plotly_chart(fig, use_container_width=True)
