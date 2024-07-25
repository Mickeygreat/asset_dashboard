import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Function to fetch data
def fetch_index_data(tickers):
    data = []
    for label, ticker in tickers.items():
        try:
            ticker_data = yf.Ticker(ticker).history(period="1d")
            current_value = ticker_data['Close'][-1]
            data.append({'Country': label, 'Index': ticker, 'Value': current_value})
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return pd.DataFrame(data)

# Define tickers for major stock indices
tickers = {
    'United States': '^GSPC',  # S&P 500
    'China': '000001.SS',      # Shanghai Composite
    'Japan': '^N225',          # Nikkei 225
    'Germany': '^GDAXI',       # DAX
    'United Kingdom': '^FTSE'  # FTSE 100
}

# Fetch data
df = fetch_index_data(tickers)

# Create an interactive choropleth map
fig = px.choropleth(
    df,
    locations="Country",
    locationmode='country names',
    color="Value",
    hover_name="Index",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Stock Exchange Indices by Country",
    labels={'Value': 'Index Value'}
)

# Add some interactivity
fig.update_geos(
    projection_type="natural earth",
    showcoastlines=True,
    coastlinecolor="Black",
    showland=True,
    landcolor="LightGray",
    showocean=True,
    oceancolor="LightBlue"
)

# Streamlit app
st.title("Global Stock Exchange Index Dashboard")
st.plotly_chart(fig, use_container_width=True)
