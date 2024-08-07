import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

# Define the data
data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada', 'South Korea', 'Russia', 'Australia', 'Spain', 'Indonesia', 'Mexico', 'Turkey', 'Switzerland', 'Sweden', 'Poland', 'Netherlands', 'Norway', 'Belgium', 'Thailand', 'Austria', 'Saudi Arabia', 'Israel', 'Ireland', 'Denmark', 'Singapore', 'Hong Kong'],
    'Index': ['^GSPC', '000001.SS', '^N225', '^GDAXI', '^FTSE', '^NSEI', '^FCHI', '^BVSP', 'FTSEMIB.MI', '^GSPTSE', '^KS11', 'IMOEX.ME', '^AORD', '^IBEX', '^JKSE', '^MXX', '^XU100.IS', '^SSMI', '^OMXS30', 'WIG.WA', '^AEX', '^OSEAX', '^BFX', '^SET', '^ATX', '^TASI.SR', '^TA125.TA', '^ISEQ', '^KS11', '^STI', '^HSI'],
    'Latitude': [37.7749, 39.9042, 35.6762, 51.1657, 51.509865, 20.5937, 46.2276, -14.2350, 43.1719, 43.6532, 36.3301, 61.5240, -33.8651, 40.4637, -6.1745, 19.4326, 38.9637, 46.9480, 59.3343, 51.9194, 52.3702, 59.9139, 50.8503, 13.7465, 24.7136, 31.7833, 53.3478, 55.6761, 1.3521, 1.2897, 22.3964],  
    'Longitude': [-122.4194, 116.4074, 139.6503, 10.4515, -0.118092, 77.1025, 2.2137, -51.9253, 12.5050, -79.3832, 127.9944, 105.3188, 151.2059, -3.7492, 106.8650, -99.1332, 35.2433, 7.4474, 18.0706, 19.1451, 4.8952, 10.7564, 5.4200, 100.5068, 46.6753, 35.2057, -6.2603, 12.5683, 103.8565, 114.1734, 114.1734],  
    'Value': [None] * 31  
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to fetch stock index values
@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_index_values(tickers):
    values = []
    for ticker in tickers:
        try:
            ticker_data = yf.Ticker(ticker).history(period="1d")
            current_value = ticker_data['Close'][-1]
            values.append(current_value)
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            values.append(None)  # Append None if there's an error
    return values

# Fetch stock index values
df['Value'] = fetch_index_values(df['Index'])

# Create a scatter map using Plotly
fig = px.scatter_geo(df,
                     lat='Latitude',
                     lon='Longitude',
                     hover_name='Country',
                     hover_data={'Index': True, 'Value': True, 'Latitude': False, 'Longitude': False},
                     projection='natural earth',
                     title="Stock Exchanges Around the World")

# Add country names
for i, row in df.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row['Longitude']],
        lat=[row['Latitude']],
        text=row['Country'],
        mode='text',
        showlegend=False,
        textposition="top center",
        textfont=dict(
            size=10,
            color="black"
        )
    ))

# Customize layout to match st.map style and make ocean blue
fig.update_layout(
    height=800, 
    margin={"r":0,"t":0,"l":0,"b":0},
    geo=dict(
        landcolor='rgb(217, 217, 217)',
        oceancolor='rgb(173, 216, 230)',  # Light blue color for the ocean
        showland=True,
        showocean=True,
        showcountries=True,
        countrycolor='rgb(204, 204, 204)',
        coastlinecolor='rgb(102, 102, 102)'
    )
)

# Display the map in Streamlit
st.title("Stock Exchanges Around the World")
st.plotly_chart(fig, use_container_width=True)

# Display DataFrame with additional information
st.write("Stock Index Values:")
st.dataframe(df[['Country', 'Index', 'Value']])
