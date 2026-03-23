
import MetaTrader5 as mt5

CONFIG = {

    "SYMBOLS":[
        "EURUSD","GBPUSD","USDJPY",
        "AUDUSD","USDCAD","USDCHF",
        "NZDUSD","EURJPY"
    ],

    "TOTAL_TRADE_PER_SYMBOL":3,

    "TREND_TIMEFRAME": mt5.TIMEFRAME_H1,
    "ENTRY_TIMEFRAME": mt5.TIMEFRAME_M1,

    "SCAN_INTERVAL":60,

    "RISK_PER_TRADE":0.01,

    "MODE": "SCALP",   # or "SWING"

    "ATR_MULT_SL":1.5,
    "ATR_MULT_TP":2.5,

    "STOP_LOSS_PIPS": 10,
    "TAKE_PROFIT_PIPS": 12,

    "AI_THRESHOLD":0.55,

    "SESSION_START":6,#12,
    "SESSION_END":21,

    "MAX_SPREAD":30
}
