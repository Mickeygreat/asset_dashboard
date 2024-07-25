import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz
from pytz import timezone

# Define the data
data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'United States'],
    'Index': ['^GSPC', '000001.SS', '^N225', '^GDAXI', '^FTSE', '^DJI'],
    'Latitude': [37.7749, 39.9042, 35.6762, 51.1657, 51.509865, 37.7749],
    'Longitude': [-122.4194, 116.4074, 139.6503, 10.4515, -0.118092, -122.4194],
    'Currency': ['USD', 'CNY', 'JPY', 'EUR', 'GBP', 'USD'],
    'Open Hour': [9, 9, 9, 9, 8, 9],  # Example opening hours for each index (24-hour format)
    'Open Minute': [0, 0, 0, 0, 0, 0],  # Example opening minutes
    'Value': [None] * 6  # Placeholder for index values
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
df['Value'] = fetch_index_values(df['Index'])

# Function to calculate local time for each stock exchange
def calculate_local_times(timezone_dict):
    now = datetime.utcnow()
    local_times = {}
    
    for idx, row in df.iterrows():
        tz = timezone_dict.get(row['Country'])
        if tz:
            local_time = now.astimezone(tz)
            local_times[row['Index']] = local_time
        else:
            local_times[row['Index']] = now  # Default to UTC if no timezone available
    return local_times

# Define timezones for each country
timezones = {
    'United States': timezone('America/New_York'),
    'China': timezone('Asia/Shanghai'),
    'Japan': timezone('Asia/Tokyo'),
    'Germany': timezone('Europe/Berlin'),
    'United Kingdom': timezone('Europe/London')
}

# Calculate local times
local_times = calculate_local_times(timezones)

# Determine the most relevant index to center the globe
def find_center_index(local_times):
    current_time = datetime.utcnow().astimezone(timezone('UTC'))
    best_index = None
    min_diff = float('inf')
    
    for idx, local_time in local_times.items():
        exchange_open_time = local_time.replace(hour=df.loc[df['Index'] == idx, 'Open Hour'].values[0],
                                                minute=df.loc[df['Index'] == idx, 'Open Minute'].values[0],
                                                second=0, microsecond=0)
        time_diff = abs((current_time - exchange_open_time).total_seconds())
        if time_diff < min_diff:
            min_diff = time_diff
            best_index = idx
    
    return best_index

# Find the center index
center_index = find_center_index(local_times)

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

# Center the globe on the most relevant stock exchange
center_index_data = df[df['Index'] == center_index].iloc[0]
fig.update_geos(
    projection_type="orthographic",
    center=dict(lat=center_index_data['Latitude'], lon=center_index_data['Longitude']),
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
