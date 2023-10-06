"""
stock_preducation 

"""

import pandas as pd
import numpy as np
import math
import datetime as dt
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score 
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

from itertools import cycle


def preparation(historical_prices):
    try:
        historical_prices.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close", "Adj Close":"adj close", "Price":"close", "Volume":"volume", "Vol.":"volume", "volume":"volume"}, inplace=True)
        # Drop na value
        historical_prices.dropna(inplace=True)
        if historical_prices.isna().any().any():
            raise ValueError("NaN values detected in the DataFrame.")
        # Convert date
        historical_prices['date'] = pd.to_datetime(historical_prices['date'], format="%m/%d/%Y")
        # Sorting dataset
        historical_prices.sort_values(by='date', inplace=True)
        return historical_prices
    except Exception as e:
        return f"An error occurred: {str(e)}"

def monthwise_comparision(historical_prices):
    try:
        monthvise_high= historical_prices.groupby(historical_prices['date'].dt.strftime('%B'))['high'].max()
        monthvise_low= historical_prices.groupby(historical_prices['date'].dt.strftime('%B'))['low'].min()
        return monthvise_high, monthvise_low
    except Exception as e:
        return f"An error occurred: {str(e)}"

def momentum(historical_prices):
    try:
        df_cl = np.asarray(historical_prices['close'])
        momentum = np.subtract(df_cl[10:], df_cl[:-10])
        return momentum
    except Exception as e:
        return f"An error occurred: {str(e)}"

def arron_indicator(historical_prices, period):
        ## Arron indicator
        ##The Arron indicator is composed of two lines. 
        ##Considering a time range, an up line measures the number of periods since the highest price in the range, and a down line which measures the number of periods since the lowest price.
        ##Aroon indicates a bullish behavior when the Aroon up is above the Aroon down. 
        ##The opposite case indicates a bearish price behavior, and when the two lines cross each other can signal a trend changes.
        
        ##Что такое индикатор Aroon? Индикатор Aroon — это технический индикатор, который используется для определения трендовых изменений цены актива, а также силы этого тренда. 
        ##По сути, индикатор измеряет время между максимумами и время между минимумами за определенный период времени.
    try:
        df_cl1 = np.asarray(historical_prices['close'])
        aroon_down=[(100/period)*
                 (period-np.argmax(df_cl1[t-period:t])) 
                 for t in range(period, len(df_cl1))]
        aroon_up=[(100/period)*
                   (period-np.argmin(df_cl1[t-period:t])) 
                   for t in range(period, len(df_cl1))]
        return aroon_down, aroon_up
    except Exception as e:
            return f"An error occurred: {str(e)}"

def log_returns(historical_prices):
    try:
        historical_prices['Log_returns'] = np.log(historical_prices['close']/historical_prices['close'].shift())
    except Exception as e:
            return f"An error occurred: {str(e)}"

def volatility(historical_prices):
    try:
        log_returns(historical_prices)
        volatility_year = historical_prices['Log_returns'].std()*252**.5
        volatility_percent = str(round(volatility_year, 4) * 100)
        return volatility_percent
    except Exception as e:
            return f"An error occurred: {str(e)}"

def top_20_max_log_returns(historical_prices):
    try:
        sorted_df_descending = historical_prices.sort_values(by='Log_returns', ascending=False)
        top_20_max_log_returns = sorted_df_descending.head(20)
        return top_20_max_log_returns
    except Exception as e:
            return f"An error occurred: {str(e)}"

def top_20_min_log_returns(historical_prices):
    try:
        sorted_df_ascending = historical_prices.sort_values(by='Log_returns', ascending=True)
        top_20_min_log_returns = sorted_df_ascending.head(20)
        return top_20_min_log_returns
    except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    dataframe = preparation(historical_prices = pd.read_csv("./content/1288 Historical Data.csv"))

    dataframe_monthwise =  monthwise_comparision(dataframe)

    momentum =  momentum(dataframe)

    arron_indicator =  arron_indicator(dataframe,7)

    volatility =  volatility(dataframe)

    top_20_min_log_returns =   top_20_min_log_returns(dataframe)


    top_20_max_log_returns =   top_20_max_log_returns(dataframe)

    print(dataframe_monthwise)
    print(momentum)
    print(arron_indicator)
    print(top_20_max_log_returns, top_20_min_log_returns)

