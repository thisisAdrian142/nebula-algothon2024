
# import numpy as np

# ##### TODO #########################################
# ### RENAME THIS FILE TO YOUR TEAM NAME #############
# ### IMPLEMENT 'getMyPosition' FUNCTION #############
# ### TO RUN, RUN 'eval.py' ##########################

# nInst = 50
# currentPos = np.zeros(nInst)


# def getMyPosition(prcSoFar):
#     global currentPos
#     (nins, nt) = prcSoFar.shape
#     if (nt < 2):
#         return np.zeros(nins)
#     lastRet = np.log(prcSoFar[:, -1] / prcSoFar[:, -2])
#     lNorm = np.sqrt(lastRet.dot(lastRet))
#     lastRet /= lNorm
#     rpos = np.array([int(x) for x in 5000 * lastRet / prcSoFar[:, -1]])
#     currentPos = np.array([int(x) for x in currentPos+rpos])
#     return currentPos


import numpy as np
import pandas as pd

nInst = 50
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos
    (nins, nt) = prcSoFar.shape
    if (nt < 26):  # Ensure there is enough data for the long period EMA
        return np.zeros(nins)
    
    macd_signals = np.zeros(nins)
    
    for i in range(nins):
        prices = pd.Series(prcSoFar[i, :])
        macd, signal, macd_diff = calculate_macd(prices)
        
        if macd_diff.iloc[-1] > 0:
            macd_signals[i] = 1  # Buy signal
        else:
            macd_signals[i] = -1  # Sell signal
    
    # Position sizing logic based on MACD signals
    rpos = macd_signals * 100  # Example: fixed position size of 100 shares
    
    currentPos = np.array([int(x) for x in currentPos + rpos])
    return currentPos

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    short_ema = prices.ewm(span=short_period, adjust=False).mean()
    long_ema = prices.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    macd_diff = macd - signal
    return macd, signal, macd_diff
