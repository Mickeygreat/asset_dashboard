import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Define the data
data = {
    'Stock Index': ['S&P 500', 'Dow Jones Industrial Average', 'NASDAQ Composite', 'NYSE COMPOSITE (DJ)', 'NYSE AMEX COMPOSITE INDEX',
                    'Cboe UK 100', 'Russell 2000', 'CBOE Volatility Index', 'FTSE 100', 'DAX PERFORMANCE-INDEX',
                    'CAC 40', 'ESTX 50 PR.EUR', 'Euronext 100 Index', 'BEL 20', 'MOEX Russia Index', 'Nikkei 225',
                    'HANG SENG INDEX', 'SSE Composite Index', 'Shenzhen Index', 'STI Index', 'S&P/ASX 200',
                    'ALL ORDINARIES', 'S&P BSE SENSEX', 'IDX COMPOSITE', 'FTSE Bursa Malaysia KLCI', 'S&P/NZX 50 INDEX GROSS',
                    'KOSPI Composite Index', 'TSEC weighted index', 'S&P/TSX Composite index', 'IBOVESPA', 'IPC MEXICO',
                    'S&P/CLX IPSA', 'MERVAL', 'TA-125', 'EGX 30 Price Return Index', 'Top 40 USD Net TRI Index'],
    'Ticker Symbol': ['^GSPC', '^DJI', '^IXIC', '^NYA', '^XAX',
                       '^BUK100P', '^RUT', '^VIX', '^FTSE', '^GDAXI',
                       '^FCHI', '^STOXX50E', '^N100', '^BFX', 'IMOEX.ME',
                       '^N225', '^HSI', '000001.SS', '399001.SZ', '^STI',
                       '^AXJO', '^AORD', '^BSESN', '^JKSE', '^KLSE',
                       '^NZ50', '^KS11', '^TWII', '^GSPTSE', '^BVSP',
                       '^MXX', '^IPSA', '^MERV', '^TA125.TA', '^CASE30',
                       '^JN0U.JO'],
    'Currency': ['USD', 'USD', 'USD', 'USD', 'USD',
                 'GBP', 'USD', 'USD', 'GBP', 'EUR',
                 'EUR', 'EUR', 'EUR', 'RUB', 'JPY',
                 'HKD', 'CNY', 'CNY', 'SGD', 'AUD',
                 'AUD', 'INR', 'IDR', 'MYR', 'NZD',
                 'KRW', 'TWD', 'CAD', 'BRL', 'MXN',
                 'CLP', 'ARS', 'ILS', 'EGP', 'USD'],
    'Latitude': [37.7749, 37.7749, 37.7749, 37.7749, 37.7749,
                 51.509865, 37.7749, 37.7749, 51.509865, 51.1657,
                 48.8566, 48.8566, 48.8566, 50.8503, 55.7558,
                 35.6762, 22.3964, 31.2304, 1.3521, -33.8688,
                 -33.8688, 19.0760, -6.2146, 3.139, -40.9006,
                 37.5665, 23.6978, 45.4215, -23.5505, 19.4326,
                 -33.4489, 32.0853, 30.0444, -26.2041],
    'Longitude': [-122.4194, -122.4194, -122.4194, -122.4194, -122.4194,
                  -0.118092, -122.4194, -122.4194, -0.118092, 10.4515,
                  2.3522, 2.3522, 2.3522, 4.3488, 37.6173,
                  114.1694, 113.7633, 121.4737, 103.8198, 151.2093,
                  151.2093, 72.8777, 106.8456, 101.6869, 174.7762,
                  126.978, 120.9605, -79.3832, -46.6333, -99.1332,
                  -70.6483, 34.7902, 31.2357, 28.0472, 28.0472],
    'Value': [None] * 36  # Placeholder for index values
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to fetch stock index values
def fetch_index_values(tickers):
    values = []
    for ticker in tickers:
        try:
            ticker_data = yf.Ticker(ticker).history(period="1d")
            current_value = ticker_data['Close'][-1]
            values.append(current_value)
        except Exception as e:
            values.append(None)  # Append None if there's an error
            print(f"Error fetching data for {ticker}: {e}")
    return values

# Fetch stock index values
df['Value'] = fetch_index_values(df['Ticker Symbol'])

# Plot map using Plotly
st.title("Interactive Globe View of Stock Exchanges")

fig = go.Figure()

# Add scattergeo trace for the globe view
fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df['Stock Index'] + '<br>Index: ' + df['Ticker Symbol'] + '<br>Value: ' + df['Value'].astype(str),
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
