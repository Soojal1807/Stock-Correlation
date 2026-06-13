import numpy as np
import pandas as pd

def compute_covariance(returns: pd.DataFrame) -> pd.DataFrame:
    R = returns.values
    R_demeaned = R - R.mean(axis=0)
    T = R_demeaned.shape[0]
    cov = (R_demeaned.T @ R_demeaned) / (T - 1)
    return pd.DataFrame(cov, index=returns.columns, columns=returns.columns)

def compute_correlation(cov: pd.DataFrame) -> pd.DataFrame:
    std = np.sqrt(np.diag(cov.values))
    D_inv = np.diag(1.0 / std)
    corr = D_inv @ cov.values @ D_inv
    return pd.DataFrame(corr, index=cov.index, columns=cov.columns)
