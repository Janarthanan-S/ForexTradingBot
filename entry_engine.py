
class EntryEngine:

    @staticmethod
    def signal(df, trend):

        prev = df.iloc[-1]

        rsi = prev["rsi"]
        price = prev["close"]
        ema20 = df["close"].ewm(span=20).mean().iloc[-1]

        if trend == "BULL":

            if rsi < 45 and abs(price - ema20) < 0.0005:
                return "BUY"

        if trend == "BEAR":

            if rsi > 55 and abs(price - ema20) < 0.0005:
                return "SELL"

        return None
