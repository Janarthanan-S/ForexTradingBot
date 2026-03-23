
class FeatureEngine:

    @staticmethod
    def compute(df):

        close = df["close"]

        df["ema50"] = close.ewm(span=50).mean()
        df["ema200"] = close.ewm(span=200).mean()

        delta = close.diff()

        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()

        rs = gain / loss
        df["rsi"] = 100 - (100/(1+rs))

        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        df["macd"] = ema12 - ema26

        df["bb_mid"] = close.rolling(20).mean()
        std = close.rolling(20).std()

        df["bb_upper"] = df["bb_mid"] + 2*std
        df["bb_lower"] = df["bb_mid"] - 2*std

        df["atr"] = (df["high"] - df["low"]).rolling(14).mean()

        return df
