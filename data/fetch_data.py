import yfinance as yf
import pandas as pd
from typing import List, Tuple

def fetch_price_data(tickers: List[str], start: str, end: str) -> pd.DataFrame:
    """
    Fetch adjusted close prices for a list of tickers.

    Args:
        tickers: List of stock tickers.
        start: Start date in 'YYYY-MM-DD'.
        end: End date in 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Adjusted close prices, indexed by date.
    """
    tickers = tickers if isinstance(tickers, list) else [tickers]
    data = yf.download(tickers, start=start, end=end, progress=False, group_by='ticker', auto_adjust=True)

    # Handle multiple vs single ticker format
    if len(tickers) == 1:
        # Single ticker — flat columns
        df = data if isinstance(data, pd.DataFrame) else data[tickers[0]]
        df = df[["Close"]]  # use "Close" since auto_adjust is True
        df.columns = [tickers[0]]
    else:
        # Multiple tickers — data[ticker]["Close"]
        df = pd.DataFrame()
        for ticker in tickers:
            try:
                close_series = data[ticker]["Close"]
                df[ticker] = close_series
            except KeyError:
                print(f"Warning: 'Close' not found for {ticker}. Skipping.")
    
    return df.dropna(how="all")

def compute_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns from price data.

    Args:
        price_df: Price DataFrame with dates as index.

    Returns:
        pd.DataFrame: Daily returns.
    """
    return price_df.pct_change().dropna()

# Example usage (only runs when executing this file directly)
if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    prices = fetch_price_data(tickers, "2020-01-01", "2023-12-31")
    returns = compute_returns(prices)

    print("Price data:")
    print(prices.head())
    print("\nDaily returns:")
    print(returns.head())
