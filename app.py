import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📈 Stock Market Dashboard")

st.markdown("Track live stock prices and visualize market trends.")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Dashboard Settings")

ticker = st.sidebar.text_input("Enter Stock Symbol", "AAPL")

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=3
)

# -----------------------------
# LOAD DATA
# -----------------------------
stock = yf.Ticker(ticker)

data = stock.history(period=period)

# Check if data exists
if data.empty:
    st.error("Invalid stock symbol.")
    st.stop()

# -----------------------------
# COMPANY INFO
# -----------------------------
info = stock.info

company_name = info.get("longName", ticker)

st.subheader(company_name)

# -----------------------------
# METRICS
# -----------------------------
current_price = data["Close"].iloc[-1]
previous_close = data["Close"].iloc[-2]

price_change = current_price - previous_close
percent_change = (price_change / previous_close) * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"${current_price:.2f}",
    f"{percent_change:.2f}%"
)

col2.metric(
    "Day High",
    f"${data['High'].iloc[-1]:.2f}"
)

col3.metric(
    "Day Low",
    f"${data['Low'].iloc[-1]:.2f}"
)

# -----------------------------
# MOVING AVERAGES
# -----------------------------
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()

# -----------------------------
# CANDLESTICK CHART
# -----------------------------
st.subheader("Candlestick Chart")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Candlestick"
    )
)

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA50"],
        mode="lines",
        name="MA50"
    )
)

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA200"],
        mode="lines",
        name="MA200"
    )
)

fig.update_layout(
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# HISTORICAL DATA
# -----------------------------
st.subheader("Historical Data")

st.dataframe(data)

# -----------------------------
# DOWNLOAD CSV
# -----------------------------
csv = data.to_csv().encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{ticker}_stock_data.csv",
    mime="text/csv"
)

# -----------------------------
# COMPANY DETAILS
# -----------------------------
st.subheader("Company Information")

st.write(f"**Sector:** {info.get('sector', 'N/A')}")
st.write(f"**Industry:** {info.get('industry', 'N/A')}")

summary = info.get("longBusinessSummary", "No summary available.")

st.write(summary)
