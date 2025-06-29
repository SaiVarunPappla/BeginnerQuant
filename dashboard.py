import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Streamlit Page Config
st.set_page_config(page_title="📈 BeginnerQuant Dashboard", layout="wide")

# Sidebar
with st.sidebar:
    st.title("📙 About BeginnerQuant")
    st.markdown("""
    This dashboard analyzes trading strategies:
    - ✅ SMA Crossover
    - ✅ RSI Overbought/Oversold
    - ✅ MACD Signal Line

    Built using Python, Streamlit, and Plotly.
    """)

# Title
st.title("📊 BeginnerQuant Trading Dashboard")

# User input
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, BTC-USD, RELIANCE.NS)", "AAPL").upper()

# Load data
data = yf.download(symbol, start="2023-01-01", end="2024-12-31")
data.dropna(inplace=True)

# Indicators
# SMA
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# RSI
delta = data['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))
data['RSI_Signal'] = 0
data.loc[data['RSI'] < 30, 'RSI_Signal'] = 1
data.loc[data['RSI'] > 70, 'RSI_Signal'] = -1

# MACD
ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = ema_12 - ema_26
data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
data['MACD_Signal_Type'] = 0
data.loc[data['MACD'] > data['MACD_Signal'], 'MACD_Signal_Type'] = 1
data.loc[data['MACD'] < data['MACD_Signal'], 'MACD_Signal_Type'] = -1

# SMA Strategy Signals
data['Signal'] = 0
data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1
data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1

# Backtests
initial_balance = 100000

# SMA Backtest
cash = initial_balance
shares = 0
portfolio_values = []
for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    signal = int(data['Signal'].iloc[i])
    if signal == 1 and cash > 0:
        shares = cash / price
        cash = 0
    elif signal == -1 and shares > 0:
        cash = shares * price
        shares = 0
    total_value = cash + (shares * price)
    portfolio_values.append(total_value)
data['SMA_Portfolio'] = portfolio_values

# RSI Backtest
cash = initial_balance
shares = 0
rsi_values = []
for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    signal = int(data['RSI_Signal'].iloc[i])
    if signal == 1 and cash > 0:
        shares = cash / price
        cash = 0
    elif signal == -1 and shares > 0:
        cash = shares * price
        shares = 0
    rsi_values.append(cash + shares * price)
data['RSI_Portfolio'] = rsi_values

# MACD Backtest
cash = initial_balance
shares = 0
macd_values = []
for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    signal = int(data['MACD_Signal_Type'].iloc[i])
    if signal == 1 and cash > 0:
        shares = cash / price
        cash = 0
    elif signal == -1 and shares > 0:
        cash = shares * price
        shares = 0
    macd_values.append(cash + shares * price)
data['MACD_Portfolio'] = macd_values

# Summary Metrics
st.markdown("---")
st.subheader(f"📊 Final Portfolio Summary for `{symbol}`")
col1, col2, col3 = st.columns(3)
col1.metric("SMA Strategy", f"₹{data['SMA_Portfolio'].iloc[-1]:,.2f}",
            f"{((data['SMA_Portfolio'].iloc[-1] - initial_balance) / initial_balance) * 100:.2f}%")
col2.metric("RSI Strategy", f"₹{data['RSI_Portfolio'].iloc[-1]:,.2f}",
            f"{((data['RSI_Portfolio'].iloc[-1] - initial_balance) / initial_balance) * 100:.2f}%")
col3.metric("MACD Strategy", f"₹{data['MACD_Portfolio'].iloc[-1]:,.2f}",
            f"{((data['MACD_Portfolio'].iloc[-1] - initial_balance) / initial_balance) * 100:.2f}%")

# Charts
st.markdown("---")
st.subheader("📊 Strategy Portfolio Growth")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_Portfolio'], name='SMA Portfolio'))
fig.add_trace(go.Scatter(x=data.index, y=data['RSI_Portfolio'], name='RSI Portfolio'))
fig.add_trace(go.Scatter(x=data.index, y=data['MACD_Portfolio'], name='MACD Portfolio'))
fig.update_layout(title="Portfolio Values Over Time", xaxis_title="Date", yaxis_title="Portfolio Value (₹)",
                  legend=dict(x=0.01, y=0.99), height=500)
st.plotly_chart(fig, use_container_width=True)

# Raw data expander
with st.expander("🔍 View Raw Data"):
    st.dataframe(data.tail(50))

# Download CSV
st.markdown("---")
st.markdown("### 📅 Download Strategy Results")
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", csv, file_name=f"{symbol}_strategies.csv", mime='text/csv')
