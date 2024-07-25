import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Define the data with stock exchange indices
data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom'],
    'Index': ['^DJI', '000001.SS', '^N225', '^GDAXI', '^FTSE'],
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
            df.at[i, 'Value'] = 'N/A'
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
    text=df['Country'] + '<br>Index: ' + df['Index'] + '<br>Value: ' + df['Value'].astype(str) + '%',
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
