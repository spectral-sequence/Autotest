# bollinger_bands.py
import talib

def calculate_bollinger_bands(close_prices, window=20, num_of_std=2):
    upper_band, middle_band, lower_band = talib.BBANDS(
        close_prices, timeperiod=window, nbdevup=num_of_std, nbdevdn=num_of_std, matype=0)
    return upper_band, middle_band, lower_band