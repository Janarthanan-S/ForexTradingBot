
class TrendEngine:

    @staticmethod
    def get_trend(df):

        ema50 = df["ema50"]
        ema200 = df["ema200"]

        if ema50.iloc[-1] > ema200.iloc[-1]:
            return "BULL"

        if ema50.iloc[-1] < ema200.iloc[-1]:
            return "BEAR"

        return None
