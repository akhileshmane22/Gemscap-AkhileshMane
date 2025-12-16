import statsmodels.api as sm
import numpy as np

def hedge_ratio(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]

def spread(y, x, beta):
    return y - beta * x

def zscore(series, window):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

from statsmodels.tsa.stattools import adfuller

def adf_test(series):
    stat, pval, *_ = adfuller(series.dropna())
    return stat, pval

def rolling_corr(x, y, window):
    return x.rolling(window).corr(y)
