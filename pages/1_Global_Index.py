import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Define the data
data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada', 'South Korea', 'Russia', 'Australia', 'Spain', 'Indonesia', 'Mexico', 'Turkey', 'Switzerland', 'Sweden', 'Poland', 'Netherlands', 'Norway', 'Belgium', 'Thailand', 'Austria', 'Saudi Arabia', 'Israel', 'Ireland', 'Denmark', 'Singapore', 'Hong Kong'],
    'Index': ['^GSPC', '000001.SS', '^N225', '^GDAXI', '^FTSE', '^NSEI', '^FCHI', '^BVSP', 'FTSEMIB.MI', '^GSPTSE', '^KS11', 'IMOEX.ME', '^AORD', '^IBEX', '^JKSE', '^MXX', '^XU100.IS', '^SSMI', '^OMXS30', 'WIG.WA', '^AEX', '^OSEAX', '^BFX', '^SET', '^ATX', '^TASI.SR', '^TA125.TA', '^ISEQ', '^KS11', '^STI', '^HSI'],
    'Latitude': [37.7749, 39.9042, 35.6762, 51.1657, 51.509865, 20.5937, 46.2276, -14.2350, 43.1719, 43.6532, 36.3301, 61.5240, -33.8651, 40.4637, -6.1745, 19.4326, 38.9637, 46.9480, 59.3343, 51.9194, 52.3702, 59.9139, 50.8503, 13.7465, 24.7136, 31.7833, 53.3478, 55.6761, 1.3521, 1.2897, 22.3964],  
    'Longitude': [-122.4194, 116.4074, 139.6503, 10.4515, -0.118092, 77.1025, 2.2137, -51.9253, 12.5050, -79.3832, 127.9944, 105.3188, 151.2059, -3.7492, 106.8650, -99.1332, 35.2433, 7.4474, 18.0706, 19.1451, 4.8952, 10.7564, 5.4200, 100.5068, 46.6753, 35.2057, -6.2603, 12.5683, 103.8565, 114.1734, 114.1734],  
    'Value': [None] * 31  
}

# st.write(len(data['Country']))  # Should print 30
# st.write(len(data['Index']))    # Should print 30
# st.write(len(data['Latitude'])) # Should print 30
# st.write(len(data['Longitude'])) # Should print 30
# st.write(len(data['Value']))    # Should print 30

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to fetch stock index values
@st.cache(ttl=60)  # Cache for 1 minute
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

# Plot map using Plotly
st.title("Interactive Globe View of Stock Exchanges")

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df['Country'],
    mode='text',
    hoverinfo='text',
    hovertext=df['Index'] + '<br>Value: ' + df['Value'].astype(str),
    textfont=dict(
        color='black',
        family='Arial',
        size=18,  # Increased font size
        weight='bold'  # Made font bold
    ),
    textposition='middle center'  # Adjusted text position
))

# adding some padding or spacing between the text elements to prevent them from overlapping
# text=df['Country'] + '<br><br>Index: ' + df['Index'] + '<br><br>Value: ' + df['Value'].astype(str)

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
