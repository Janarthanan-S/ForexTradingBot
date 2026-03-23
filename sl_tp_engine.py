from config import CONFIG
import MetaTrader5 as mt5

class SLTPEngine:

    @staticmethod
    def compute(symbol, df, direction):

        tick = mt5.symbol_info_tick(symbol)
        info = mt5.symbol_info(symbol)

        point = info.point
        pip = point * 10

        price = tick.ask if direction == "BUY" else tick.bid

        # =========================
        # SCALPING MODE
        # =========================
        if CONFIG["MODE"] == "SCALP":

            sl_pips = CONFIG["STOP_LOSS_PIPS"]
            tp_pips = CONFIG["TAKE_PROFIT_PIPS"]

            if direction == "BUY":
                sl = price - sl_pips * pip
                tp = price + tp_pips * pip
            else:
                sl = price + sl_pips * pip
                tp = price - tp_pips * pip

            return sl, tp

        # =========================
        # SWING MODE (ATR)
        # =========================
        else:

            atr = df["atr"].iloc[-1]

            sl_dist = atr * CONFIG["ATR_MULT_SL"]
            tp_dist = atr * CONFIG["ATR_MULT_TP"]

            if direction == "BUY":
                sl = price - sl_dist
                tp = price + tp_dist
            else:
                sl = price + sl_dist
                tp = price - tp_dist

            return sl, tp