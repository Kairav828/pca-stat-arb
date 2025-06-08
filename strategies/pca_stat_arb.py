import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import statsmodels.api as sm

def run_pca(returns_df: pd.DataFrame, n_components: int = 3):
    """
    Runs PCA on the stock returns data.

    Args:
        returns_df: DataFrame of returns (stocks as columns).
        n_components: Number of principal components to retain.

    Returns:
        np.ndarray: Transformed principal components.
        PCA object: Fitted PCA model for further inspection.
    """
    pca = PCA(n_components=n_components)
    pcs = pca.fit_transform(returns_df)
    return pcs, pca

def regress_target_on_pcs(target_returns: pd.Series, pcs: np.ndarray):
    """
    Regresses a target stock's returns on the principal components.

    Args:
        target_returns: Return series of the target stock.
        pcs: Principal components from PCA.

    Returns:
        pd.Series: Residuals from the regression (unexplained return).
    """
    X = sm.add_constant(pcs)
    model = sm.OLS(target_returns.values, X).fit()
    residuals = model.resid
    return pd.Series(residuals, index=target_returns.index)

def compute_z_scores(residuals: pd.Series, window: int = 20):
    """
    Computes the rolling z-score of residuals.

    Args:
        residuals: Regression residuals over time.
        window: Rolling window for mean and std.

    Returns:
        pd.Series: Z-score series.
    """
    mean = residuals.rolling(window=window).mean()
    std = residuals.rolling(window=window).std()
    z_scores = (residuals - mean) / std
    return z_scores
