# 📊 BeginnerQuant: Algorithmic Trading Strategies with Streamlit Dashboard

![Streamlit Screenshot 1](streamlit1.png)
![Streamlit Screenshot 2](streamlit2.png)

---

Welcome to **BeginnerQuant** – a beginner-friendly but powerful algorithmic trading project designed to **simulate and visualize trading strategies** like **SMA (Simple Moving Average)**, **RSI (Relative Strength Index)**, and **MACD (Moving Average Convergence Divergence)**.

🔗 **Live App**: [Click to View Streamlit Dashboard](https://beginnerquant-gg3kca3rc73rjtr26n4hyj.streamlit.app/)

---

##  Features

 **User-Interactive Dashboard** with Streamlit
 Backtesting strategies with custom logic
 Multi-Stock support (`AAPL`, `TSLA`, `RELIANCE.NS`, `BTC-USD`, etc.)
 Easy CSV export of trading results
 Clean GitHub structure and modular code

---

##  Strategies Implemented

### 1. **SMA Crossover**

* Buy when 20-day SMA crosses above 50-day SMA
* Sell when 20-day SMA drops below 50-day SMA

### 2. **RSI (Relative Strength Index)**

* Buy when RSI < 30 (oversold)
* Sell when RSI > 70 (overbought)

### 3. **MACD (Moving Average Convergence Divergence)**

* Buy when MACD crosses above signal line
* Sell when MACD crosses below signal line

---

## Project Structure

```
BeginnerQuant/
│
├── trading_strategy.py      # Strategy backtesting logic
├── dashboard.py             # Streamlit app for visualization
├── requirements.txt         # Dependencies for the project
├── README.md                # Project documentation
├── streamlit1.png           # Dashboard screenshot 1
├── streamlit2.png           # Dashboard screenshot 2
└── RELIANCE.NS_trading_results.csv  # Sample export file
```

---

##  Exported Results

* Portfolio value & performance saved as `.csv` file
* Strategy-wise final value, return %, and comparison

---

##  How This Helps Your Career

If you're a beginner exploring **quantitative finance**, **algorithmic trading**, or **data-driven investing**, this project will help you:

Learn real-world indicators and apply them in code
Understand strategy simulation from scratch
Build and deploy dashboards for portfolio analysis
Strengthen your Git/GitHub & Streamlit skills

---

##  How to Run This Project

```bash
# 1. Clone the repository
https://github.com/SaiVarunPappla/BeginnerQuant.git

# 2. Navigate into project
cd BeginnerQuant

# 3. Install requirements
pip install -r requirements.txt

# 4. Run Streamlit dashboard
streamlit run dashboard.py
```

---

## Built With

* Python 
* Pandas, NumPy, Matplotlib
* yFinance 
* Streamlit 
* Git & GitHub

---

##  Acknowledgements

Big thanks to open-source finance libraries, the Streamlit community, and every beginner out there trying to learn and build!

---

> ⭐ Star this repo if you found it helpful or inspiring!
