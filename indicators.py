# Some basic functions for trading strategies
# Alec Myres
# MATH G4073 - Columbia University

# Load useful python libraries
import numpy as np
import pandas as pd

# Load csv as a DataFrame object
df = pd.read_csv('/Users/alecmyres/Documents/G4073_Qnt_Mthds/data.csv')

# Simple moving average
def get_sma(df_col, w = 20):
  return pd.rolling_mean(df_col, window = w)

# Exponentially weighted moving average
def get_ema(df_col, alpha = 0.95):
  s = (1.0 + alpha)/(1.0 - alpha)
  return pd.ewma(df_col, span = s)

# Bollinger bands
def get_bollinger(df_col, w = 20, s = 2):
  bandwidth = pd.rolling_std(df_col, window = w)
  upper = get_sma(df_col, w)+bandwidth*s
  lower = get_sma(df_col, w)-bandwidth*s
  return upper, lower

# Momentum (differences)
def get_mom(df_col, per = 10):
  roll = (np.roll(df_col, 0)-np.roll(df_col, per))[per:]
  fill = [np.nan]*per
  return pd.Series(fill+list(roll))

# Momentum EMA
def get_mom_ema(df_col, per = 10, alpha = 0.95):
  mom = get_mom(df_col, per)
  ema_mom = get_ema(mom, alpha)
  return mom/ema_mom

# The above functions take an array as an argument, with other optional parameters
# Each function returns an array, which can be used in other functions

# Add columns to DataFrame
df['sma20']  = get_sma(df['Price'])
df['ema']    = get_ema(df['Price'])
df['mom10']  = get_mom(df['Price'])
df['momEMA'] = get_mom_ema(df['Price'])
df['bollUpper'], df['bollLower'] = get_bollinger(df['Price'])

# ----------------------------------------
# More indicators by Yeyun Chen

# Acceleration (difference of price change)
def get_accel(df_col, per = 10):
    mom_t = get_mom(df_col, per)[per:]
    roll = (np.roll(mom_t, 0)-np.roll(mom_t, 1))[1: ]
    fill = [np.nan]*(per+1)
    return pd.Series(fill+list(roll))
  
# rate of change  
def get_roc(df_col, per = 10):
  roll = ((get_mom(df_col, per))/(np.roll(df_col, per)))[per:]
  fill = [np.nan]*per
  return pd.Series(fill+list(roll))

# moving average convergence divergence
# difference between two moving avergaes of slow(s) and fast(f) periods
def get_macd(df_col, s = 26, f = 12):
    return(pd.ewma(df_col, span = s)-pd.ewma(df_col, span = f))

# MACD signal line: moving average of MACD of past n periods.
def get_macds(df_col, s = 26, f = 12, n = 9):
    return(pd.ewma(get_macd(df_col, s, f), span = n))

# Relative strength index
def get_rsi(df_col, per = 10):
    p_up = [np.nan]*df_col.size
    p_dn = [np.nan]*df_col.size
    for i in range(1, df_col.size):
        if (df_col[i] - df_col[i-1] > 0):
            p_up[i] = df_col[i]
        elif (df_col[i] - df_col[i-1] < 0):
            p_dn[i] = df_col[i]

    ma_up = [np.nan]*df_col.size
    ma_dn = [np.nan]*df_col.size
    rsi = [np.nan]*df_col.size
    for j in range(per+1, df_col.size):
        ma_up[j] = np.nanmean(p_up[j-per:j])
        ma_dn[j] = np.nanmean(p_dn[j-per:j])
        rsi[j] = 100-100/(1+ma_up[j]/ma_dn[j])
    fill = [np.nan]*(per+1)
    return pd.Series(fill+list(rsi))
        

# The above functions take an array as an argument, with other optional parameters
# Each function returns an array, which can be used in other functions

# Add columns to DataFrame
df['accel'] = get_accel(df['Price'])
df['roc'] = get_roc(df['Price'])
df['macd'] = get_macd(df['Price'])
df['macds'] = get_macds(df['Price'])
df['rsi'] = get_rsi(df['Price'])
