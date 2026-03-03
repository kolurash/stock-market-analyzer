import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("📈 Stock Market Analyzer")

st.markdown("""
Welcome to the **Stock Market Analyzer**!  
This app helps investors and students understand stock trends using past data.  
You can enter any stock ticker (like `AAPL` for Apple, `TSLA` for Tesla, `RELIANCE.NS` for Reliance, or `^NSEI` for Nifty 50).  
It will show you:
- Historical stock data (Open, High, Low, Close, Volume)
- Closing price chart
- Moving averages (20-day and 50-day)
- A simple decision suggestion: **Invest, Exit, or Wait**
""")


# User input for ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, RELIANCE.NS, ^BSESN)", "AAPL")

if ticker:
    # Fetch last 1 year of data
    data = yf.download(ticker, period="1y")

    if isinstance(data.columns, pd.MultiIndex): 
        data.columns = [col[0] for col in data.columns]
    
    st.subheader(f"{ticker} Stock Data (Last 1 Year)")
    st.write(data.tail())  # show last 5 rows

    st.markdown("""
**Understanding the Table Columns:**
- **Open**: Price at which the stock started trading that day.
- **High**: Highest price reached during the day.
- **Low**: Lowest price reached during the day.
- **Close**: Price at which the stock ended trading that day.
- **Volume**: Number of shares traded.
""")


    # Closing price chart
    fig = px.line(data, x=data.index, y="Close", title=f"{ticker} Closing Price")
    st.plotly_chart(fig,key="closing_chart")

    st.markdown("""
**Closing Price Chart:**  
This graph shows how the stock's closing price has moved over time.  
It helps investors see overall trends and volatility.
""")


    # Moving averages
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    fig_ma = px.line(data, x=data.index, y=["Close", "MA20", "MA50"], 
                     title=f"{ticker} with Moving Averages")
    st.plotly_chart(fig_ma , key="ma_chart")

    st.markdown("""
**Moving Averages Chart:**  
- **MA20**: Average closing price over the last 20 days (short-term trend).  
- **MA50**: Average closing price over the last 50 days (medium-term trend).  
When MA20 crosses above MA50, it often signals bullish momentum.  
When MA20 crosses below MA50, it often signals bearish momentum.
""")




# --- Add decision logic here ---
decision = "Wait"  # default

latest_close = data["Close"].iloc[-1]
latest_ma20 = data["MA20"].iloc[-1]
latest_ma50 = data["MA50"].iloc[-1]
prev_ma20 = data["MA20"].iloc[-2] # yesterday's MA20

if latest_close > latest_ma20 and latest_close > latest_ma50 and latest_ma20 > prev_ma20:
    decision = "Invest"
elif latest_close < latest_ma20 and latest_close < latest_ma50 and latest_ma20 < prev_ma20:
    decision = "Exit"
else:
    decision = "Wait"

st.subheader("📊 Suggested Decision")
st.write(f"Based on current indicators: **{decision}**")

