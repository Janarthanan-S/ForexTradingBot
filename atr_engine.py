
from config import CONFIG

class ATRStops:

    @staticmethod
    def compute(df, direction):

        atr = df["atr"].iloc[-1]
        price = df["close"].iloc[-1]

        sl_dist = atr * CONFIG["ATR_MULT_SL"]
        tp_dist = atr * CONFIG["ATR_MULT_TP"]

        if direction == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
        else:
            sl = price + sl_dist
            tp = price - tp_dist

        return sl, tp
