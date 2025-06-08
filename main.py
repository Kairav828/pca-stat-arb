from data.fetch_data import fetch_price_data, compute_returns
from strategies.pca_stat_arb import run_pca, regress_target_on_pcs, compute_z_scores

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
prices = fetch_price_data(tickers, "2020-01-01", "2023-12-31")
returns = compute_returns(prices)

# Run PCA on everything except target
target = "AAPL"
X = returns.drop(columns=[target])
y = returns[target]

pcs, _ = run_pca(X, n_components=3)
residuals = regress_target_on_pcs(y, pcs)
z_scores = compute_z_scores(residuals)

print(z_scores.tail())

from backtest.backtest_engine import backtest_zscore_strategy

bt_result = backtest_zscore_strategy(z_scores, returns[target])
print(bt_result.tail())

import matplotlib.pyplot as plt
bt_result["Cumulative Return"].plot(title=f"{target} Strategy Cumulative Return")
plt.show()

from backtest.performance_metrics import calculate_performance_metrics

metrics = calculate_performance_metrics(bt_result["Strategy PnL"])
print("\nPerformance Metrics:")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")
