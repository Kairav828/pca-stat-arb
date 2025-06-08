import pandas as pd
import numpy as np

def calculate_performance_metrics(pnl: pd.Series, risk_free_rate: float = 0.0, freq: int = 252):
    """
    Calculate key strategy performance metrics.

    Args:
        pnl: Series of strategy daily returns.
        risk_free_rate: Annual risk-free rate (as decimal).
        freq: Trading days per year.

    Returns:
        dict: Dictionary of performance metrics.
    """
    pnl = pnl.dropna()
    cumulative_return = (1 + pnl).prod() - 1
    annualized_return = (1 + cumulative_return) ** (freq / len(pnl)) - 1
    annualized_volatility = pnl.std() * np.sqrt(freq)
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility > 0 else np.nan

    # Drawdown
    cumulative = (1 + pnl).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    return {
        "Cumulative Return": cumulative_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown
    }
