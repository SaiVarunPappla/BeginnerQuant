import yfinance as yf
# ✅ Ask user for stock symbol
print("\n📥 Enter Stock Symbol (e.g., AAPL, TSLA, BTC-USD, RELIANCE.NS):")
symbol = input("🔍 Stock: ").upper().strip()
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Download stock data
data = yf.download(symbol, start='2023-01-01', end='2024-12-31')

# Step 2: Calculate moving averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Step 3: Create Buy/Sell signals
data['Signal'] = 0
# Calculate RSI
delta = data['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Create RSI signals
data['RSI_Signal'] = 0
# ✅ Calculate MACD and Signal Line
ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = ema_12 - ema_26
data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

# ✅ Create MACD Buy/Sell Signals
data['MACD_Signal_Type'] = 0
data.loc[data['MACD'] > data['MACD_Signal'], 'MACD_Signal_Type'] = 1
data.loc[data['MACD'] < data['MACD_Signal'], 'MACD_Signal_Type'] = -1

data.loc[data['RSI'] < 30, 'RSI_Signal'] = 1  # Buy when oversold
data.loc[data['RSI'] > 70, 'RSI_Signal'] = -1  # Sell when overbought

data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1
data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1

# ✅ Step 4: Backtest simulation
initial_balance = 100000.0
cash = initial_balance
shares = 0.0
portfolio_values = []
# ✅ Step 4.2: RSI Backtest simulation
# ✅ Step 4.3: MACD Backtest simulation
macd_cash = initial_balance
macd_shares = 0.0
macd_portfolio_values = []

for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    macd_signal = int(data['MACD_Signal_Type'].iloc[i])

    if macd_signal == 1 and macd_cash > 0:
        macd_shares = macd_cash / price
        macd_cash = 0
    elif macd_signal == -1 and macd_shares > 0:
        macd_cash = macd_shares * price
        macd_shares = 0

    total_macd_value = macd_cash + (macd_shares * price)
    macd_portfolio_values.append(total_macd_value)

data['MACD Portfolio Value'] = macd_portfolio_values
rsi_cash = initial_balance
rsi_shares = 0.0
rsi_portfolio_values = []

for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    rsi_signal = int(data['RSI_Signal'].iloc[i])  # use RSI signals

    if rsi_signal == 1 and rsi_cash > 0:
        rsi_shares = rsi_cash / price
        rsi_cash = 0

    elif rsi_signal == -1 and rsi_shares > 0:
        rsi_cash = rsi_shares * price
        rsi_shares = 0

    total_rsi_value = rsi_cash + (rsi_shares * price)
    rsi_portfolio_values.append(total_rsi_value)

# Save to dataframe
data['RSI Portfolio Value'] = rsi_portfolio_values


# 🔁 Loop over each row correctly
for i in range(len(data)):
    price = float(data['Close'].iloc[i])
    signal = int(data['Signal'].iloc[i])  # ✅ Convert to number

    if signal == 1 and cash > 0:
        shares = cash / price
        cash = 0

    elif signal == -1 and shares > 0:
        cash = shares * price
        shares = 0

    total_value = cash + (shares * price)
    portfolio_values.append(total_value)

# Add result to DataFrame
data['Portfolio Value'] = portfolio_values

# ✅ Step 5: Print result
final_value = portfolio_values[-1]
profit = final_value - initial_balance
return_pct = (profit / initial_balance) * 100
print(f"\n📊 Running analysis for: {symbol}\n")
print(f"\n💼 Final Portfolio Value: ₹{final_value:,.2f}")
print(f"📈 Profit: ₹{profit:,.2f} ({return_pct:.2f}%)")
rsi_final = rsi_portfolio_values[-1]
rsi_profit = rsi_final - initial_balance
rsi_return_pct = (rsi_profit / initial_balance) * 100

print(f"\n📊 RSI Strategy Portfolio Value: ₹{rsi_final:,.2f}")
macd_final = macd_portfolio_values[-1]
macd_profit = macd_final - initial_balance
macd_return_pct = (macd_profit / initial_balance) * 100

print(f"\n📊 MACD Strategy Portfolio Value: ₹{macd_final:,.2f}")
print(f"📈 MACD Strategy Profit: ₹{macd_profit:,.2f} ({macd_return_pct:.2f}%)")

print(f"📈 RSI Strategy Profit: ₹{rsi_profit:,.2f} ({rsi_return_pct:.2f}%)")


# ✅ Step 6: Plot Buy/Sell chart
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['SMA_20'], label='SMA 20', color='green')
plt.plot(data['SMA_50'], label='SMA 50', color='red')

buy_signals = data[(data['Signal'] == 1) & (data['Signal'].shift(1) != 1)]
sell_signals = data[(data['Signal'] == -1) & (data['Signal'].shift(1) != -1)]

plt.plot(buy_signals.index, data.loc[buy_signals.index, 'Close'], '^', color='green', label='Buy', markersize=10)
plt.plot(sell_signals.index, data.loc[sell_signals.index, 'Close'], 'v', color='red', label='Sell', markersize=10)

plt.title("SMA Strategy with Buy/Sell Signals")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

# ✅ Step 7: Portfolio growth chart
plt.figure(figsize=(14, 5))
plt.plot(data['Portfolio Value'], label='Portfolio Value', color='purple')
plt.title("Portfolio Growth Over Time")
plt.xlabel("Date")
plt.ylabel("₹ Value")
plt.legend()
plt.grid(True)
plt.show()
plt.figure(figsize=(14, 5))
plt.plot(data['RSI Portfolio Value'], label='RSI Portfolio', color='orange')
plt.title("RSI Strategy Portfolio Growth")
plt.xlabel("Date")
plt.ylabel("₹ Value")
plt.grid(True)
plt.legend()
plt.show()
plt.figure(figsize=(14, 5))
plt.plot(data['MACD Portfolio Value'], label='MACD Portfolio', color='teal')
plt.title("MACD Strategy Portfolio Growth")
plt.xlabel("Date")
plt.ylabel("₹ Value")
plt.grid(True)
plt.legend()
plt.show()
# ✅ Export to CSV
export_columns = [
    'Close',
    'Signal', 'Portfolio Value',
    'RSI', 'RSI_Signal', 'RSI Portfolio Value',
    'MACD', 'MACD_Signal', 'MACD_Signal_Type', 'MACD Portfolio Value'
]

# Some symbols may not have all columns due to missing values
export_data = data[export_columns].copy()

# Save as a CSV file using the stock symbol
filename = f"{symbol}_trading_results.csv"
export_data.to_csv(filename)

print(f"\n📁 Strategy results saved to: {filename}")