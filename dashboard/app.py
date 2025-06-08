import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data.fetch_data import fetch_price_data, compute_returns
from strategies.pca_stat_arb import run_pca, regress_target_on_pcs, compute_z_scores
from backtest.backtest_engine import backtest_zscore_strategy
from backtest.performance_metrics import calculate_performance_metrics

st.set_page_config(page_title="PCA StatArb Dashboard", layout="wide")

st.title("📈 PCA-Based Statistical Arbitrage Dashboard")

st.markdown("""
This dashboard demonstrates a **mean-reversion trading strategy** based on statistical relationships between related stocks.

Here's how it works:
- It looks at a group of related stocks (e.g., tech stocks like AAPL, MSFT, GOOGL).
- It finds shared trends using **Principal Component Analysis (PCA)**.
- It picks a *target stock* (e.g. AAPL), and checks when it *temporarily diverges* from the group.
- If AAPL strays too far from the trend, we assume it will snap back — and we trade on that.
- You can tweak the sliders to change how sensitive the strategy is.

**Note:** If the chart shows your strategy consistently losing money, it means the assumptions (like mean reversion) didn't hold for that time period or those stocks — a great reminder that backtesting is key in quant trading!
""")


# --- Sidebar Inputs ---
tickers = st.sidebar.text_input("Enter tickers (comma separated)", "AAPL,MSFT,GOOGL,AMZN")
ticker_list = [t.strip().upper() for t in tickers.split(",")]

target = st.sidebar.selectbox("Target stock to trade", ticker_list)
start = st.sidebar.date_input("Start date", pd.to_datetime("2020-01-01"))
end = st.sidebar.date_input("End date", pd.to_datetime("2023-12-31"))

n_components = st.sidebar.slider("PCA Components", 1, len(ticker_list)-1, 3)
entry_threshold = st.sidebar.slider("Entry Threshold (z)", 1.0, 3.0, 2.0)
exit_threshold = st.sidebar.slider("Exit Threshold (z)", 0.0, 2.0, 0.5)
z_window = st.sidebar.slider("Z-score window", 10, 60, 20)

if st.button("Run Strategy"):

    with st.spinner("Fetching data and running strategy..."):
        prices = fetch_price_data(ticker_list, str(start), str(end))
        returns = compute_returns(prices)

        X = returns.drop(columns=[target])
        y = returns[target]

        pcs, _ = run_pca(X, n_components=n_components)
        residuals = regress_target_on_pcs(y, pcs)
        z_scores = compute_z_scores(residuals, window=z_window)

        bt_result = backtest_zscore_strategy(z_scores, y, entry_threshold, exit_threshold)
        metrics = calculate_performance_metrics(bt_result["Strategy PnL"])

    st.subheader(f"📊 {target} Backtest Summary")

    # Plot
    fig, ax = plt.subplots()
    bt_result["Cumulative Return"].plot(ax=ax, title=f"{target} Strategy Cumulative Return")
    st.pyplot(fig)

    # Metrics
    st.write("### 📈 Performance Metrics")
    st.dataframe(pd.DataFrame(metrics, index=["Value"]).T)

    # Table
    st.write("### 🧾 Signal Table (Last 10 rows)")
    st.dataframe(bt_result.tail(10))
