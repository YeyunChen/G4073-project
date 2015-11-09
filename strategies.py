# Trading Strategies
# Yeyun Chen
# MATH G4073 - Columbia University

# return and data and the outcome
# 1 indicates to buy
# -1 indicates to sell

# Load useful python libraries
import numpy as np
import pandas as pd

# Load csv as a DataFrame object
df = pd.read_csv('C:/Users/asus/Desktop/Columbia Study Material/4073/Project/data.csv')

# Strategy 1: Bolliger Band
def get_strategy_bollinger(price):
    action = [np.nan]*price.size
    bollUpper, bollLower = get_bollinger(price)
    for i in range(1, price.size):
        if price[i-1] <= bollLower[i] and price[i] > bollUpper[i]:
            action[i] = -1
        elif price[i-1] >= bollLower[i] and price[i] < bollUpper[i]:
            action[i] = 1     
        else:
            action[i] = 0
    return action 

# Strategy 2: Momentum
def get_strategy_Momentum(price):
    action = [np.nan]*price.size
    mom  = get_mom(df['Price'])
    momEMA = get_mom_ema(df['Price'])
    for i in range(1, price.size):
        if np.isnan(mom[i-1]) == False and np.isnan(momEMA[i-1]) == False:
            if mom[i-1] <= momEMA[i] and mom[i] > momEMA[i]:
                action[i] = 1
            elif mom[i-1] >= momEMA[i] and mom[i] < momEMA[i]:
                action[i] = -1
            else:
                action[i] = 0
    return action         

# Strategy 3: Rate of Change
def get_strategy_ROC(price):
    action = [np.nan]*price.size
    ROC  = get_roc(df['Price'])
    for i in range(1, price.size):
        if np.isnan(ROC[i-1]) == False:
            if ROC[i-1] <= 0 and ROC[i] > 0:
                action[i] = 1
            elif ROC[i-1] >= 0 and ROC[i] < 0:
                action[i] = -1
            else:
                action[i] = 0
    return action         
    
df['action1'] = get_strategy_bollinger(df['Price'])
df['action2'] = get_strategy_Momentum(df['Price'])
df['action3'] = get_strategy_ROC(df['Price'])
    



