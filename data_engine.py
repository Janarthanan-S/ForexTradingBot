
import MetaTrader5 as mt5
import pandas as pd

class MarketData:

    @staticmethod
    def get_candles(symbol, timeframe, bars=300):

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

        if rates is None:
            return None

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")

        return df
