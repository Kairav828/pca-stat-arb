import pandas as pd

def backtest_zscore_strategy(z_scores: pd.Series,
                              returns: pd.Series,
                              entry_threshold: float = 2.0,
                              exit_threshold: float = 0.5):
    """
    Backtests a simple z-score mean reversion strategy.

    Args:
        z_scores: Z-score time series for residuals.
        returns: Actual returns of the target asset.
        entry_threshold: Threshold to enter long/short.
        exit_threshold: Threshold to exit position.

    Returns:
        pd.DataFrame: DataFrame with positions and cumulative returns.
    """
    position = 0  # 1 for long, -1 for short, 0 for neutral
    positions = []
    daily_pnl = []

    for date, z in z_scores.items():
        r = returns.get(date, 0.0)

        if position == 0:
            if z < -entry_threshold:
                position = 1  # go long
            elif z > entry_threshold:
                position = -1  # go short

        elif position == 1 and z > -exit_threshold:
            position = 0  # exit long

        elif position == -1 and z < exit_threshold:
            position = 0  # exit short

        positions.append(position)
        daily_pnl.append(position * r)

    result = pd.DataFrame({
        "Z-score": z_scores,
        "Position": positions,
        "Daily Return": returns.loc[z_scores.index],
        "Strategy PnL": daily_pnl
    })

    result["Cumulative Return"] = (1 + result["Strategy PnL"]).cumprod()
    return result
