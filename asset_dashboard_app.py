import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Define the default tickers and their labels
default_tickers = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "Gold Futures": "GC=F",
    "Oil Futures": "BZ=F",
    "10 Year T Bond Yield": "^TNX"
}

# Function to fetch and plot data
def plot_ticker(ticker, label, interval, period, chart_type, up_color, down_color):
    data = yf.download(ticker, period=period, interval=interval)
    fig = go.Figure()

    if chart_type == "Candles":
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=label,
            increasing_line_color=up_color,
            decreasing_line_color=down_color
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=label
        ))

    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker=dict(color='rgba(128, 128, 128, 0.5)')
    ))

    fig.update_layout(
        title=f"{label} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis=dict(domain=[0.2, 1]),
        yaxis2=dict(domain=[0, 0.2], title='Volume'),
        barmode='relative'
    )
    fig.update_traces(yaxis='y2', selector=dict(type='bar'))

    return fig

# Function to get current price and change percentage
def get_current_price(ticker):
    ticker_data = yf.Ticker(ticker)
    todays_data = ticker_data.history(period='1d')
    current_price = todays_data['Close'][0]
    previous_close = todays_data['Open'][0]
    change_percentage = ((current_price - previous_close) / previous_close) * 100
    return current_price, change_percentage

st.title("Financial Dashboard")

# Global interval selector
interval = st.selectbox(
    "Select interval for all charts",
    options=["15m", "1h", "4h", "1d", "3d", "1wk", "1y"],
    index=3
)

# Global period selector
period = st.selectbox(
    "Select period for all charts",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=2
)

# Chart type selector
chart_type = st.radio(
    "Select chart type for all charts",
    options=["Candles", "Line"],
    index=1  # Default to "Line" (index 1)
)

# Candlestick color selectors
if chart_type == "Candles":
    up_color = st.color_picker("Select color for upward candles", "#00ff00")
    down_color = st.color_picker("Select color for downward candles", "#ff0000")
else:
    up_color = down_color = None

# Create a grid layout for the dashboard
cols = st.columns(2)
index = 0

# Set of labels for which to omit the dollar sign
no_dollar_labels = {"Dow Jones", "Russell 2000", "NASDAQ", "S&P 500"}

for label, ticker in default_tickers.items():
    with cols[index % 2]:
        current_price, change_percentage = get_current_price(ticker)
        change_color = "green" if change_percentage > 0 else "red"

        price_display = f"${current_price:.2f}"
        if label in no_dollar_labels:
            price_display = f"{current_price:.2f}"
        
        st.markdown(f"### {label}: {price_display}")
        st.markdown(
            f"### <span style='color:{change_color};'>({change_percentage:.2f}%)</span>", unsafe_allow_html=True)

        ticker = st.text_input("", value=ticker)

        fig = plot_ticker(ticker, label, interval, period, chart_type, up_color, down_color)
        st.plotly_chart(fig, use_container_width=True)
    index += 1
