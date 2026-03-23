import time
import MetaTrader5 as mt5

from config import CONFIG
from data_engine import MarketData
from feature_engine import FeatureEngine
from trend_engine import TrendEngine
from entry_engine import EntryEngine
from sl_tp_engine import SLTPEngine
from risk_engine import RiskEngine
from execution_engine import ExecutionEngine
from session_filter import SessionFilter
from ai_filter import AIFilter
from risk_guard import RiskGuard
from mt5_codes import MT5_CODES
from logger import get_logger

log = get_logger()


def run():

    log.info("Initializing MT5...")

    if not mt5.initialize():
        log.error("MT5 initialization failed")
        return

    log.info("Bot started")

    while True:

        try:

            # ✅ Session filter
            if not SessionFilter.allowed():
                log.info("Outside trading session")
                time.sleep(300)
                continue

            account = mt5.account_info()
            balance = account.balance
            RiskGuard.initialize()

            log.info(f"Balance: {balance}")

            for symbol in CONFIG["SYMBOLS"]:
                if RiskGuard.daily_loss_exceeded():
                    log.error("Daily loss limit reached. Stopping trading.")
                    break

                positions = mt5.positions_get()

                # Limit per symbol
                symbol_positions = [
                    p for p in positions if p.symbol == symbol
                ] if positions else []

                if len(symbol_positions) >= CONFIG["TOTAL_TRADE_PER_SYMBOL"]:
                    log.warning(f"{symbol} already has maximum open trade, skipping")
                    continue

                log.info(f"Scanning {symbol}")

                # =========================
                # Spread Check
                # =========================
                tick = mt5.symbol_info_tick(symbol)
                info = mt5.symbol_info(symbol)

                if tick is None or info is None:
                    log.warning(f"{symbol} tick/info missing")
                    continue

                spread = (tick.ask - tick.bid) / info.point

                if spread > CONFIG["MAX_SPREAD"]:
                    log.warning(f"{symbol} spread too high: {spread}")
                    continue

                # =========================
                # Get Data
                # =========================
                df_trend = MarketData.get_candles(
                    symbol,
                    CONFIG["TREND_TIMEFRAME"]
                )

                df_entry = MarketData.get_candles(
                    symbol,
                    CONFIG["ENTRY_TIMEFRAME"]
                )

                if df_trend is None or df_entry is None:
                    log.warning(f"{symbol} no data")
                    continue

                df_trend = FeatureEngine.compute(df_trend)
                df_entry = FeatureEngine.compute(df_entry)

                # =========================
                # Trend
                # =========================
                trend = TrendEngine.get_trend(df_trend)

                if trend is None:
                    log.info(f"{symbol} no trend")
                    continue

                # =========================
                # Entry Signal
                # =========================
                signal = EntryEngine.signal(df_entry, trend)

                if signal is None:
                    log.info(f"{symbol} no entry signal")
                    continue

                log.info(f"{symbol} SIGNAL: {signal}")

                # =========================
                # SL / TP
                # =========================
                sl, tp = SLTPEngine.compute(symbol, df_entry, signal)

                # =========================
                # Price & Distance (FIXED)
                # =========================
                price = tick.ask if signal == "BUY" else tick.bid

                sl_distance = abs(price - sl)

                # =========================
                # AI Filter
                # =========================
                features = [
                    df_entry["rsi"].iloc[-1],
                    df_entry["macd"].iloc[-1],
                    df_entry["atr"].iloc[-1]
                ]

                probability = AIFilter.predict(features)

                log.info(f"{symbol} AI probability: {probability}")

                if AIFilter.trained and probability < CONFIG["AI_THRESHOLD"]:
                    log.info(f"{symbol} AI rejected trade")
                    continue

                # =========================
                # Lot Calculation
                # =========================
                lot = RiskEngine.calculate_lot(
                    balance,
                    CONFIG["RISK_PER_TRADE"],
                    sl_distance,
                    symbol
                )
                if lot > 0.01:
                    log.warning(f"{symbol} lot too high,lot:{lot} clamping to 0.01")
                    lot = 0.01
                log.info(
                    f"{symbol} price:{price} SL:{sl} TP:{tp} "
                    f"distance:{sl_distance} lot:{lot}"
                )

                # =========================
                # Execute Trade
                # =========================
                result = ExecutionEngine.place_trade(
                    symbol,
                    signal,
                    lot,
                    sl,
                    tp
                )
                code = result.retcode
                meaning = MT5_CODES.get(code, "UNKNOWN")
                log.info(f"{symbol} trade result: {code} ({meaning})")

                if result is None:
                    log.error(f"{symbol} order_send returned None")
                    continue

            log.info("Cycle complete. Sleeping...\n")

            time.sleep(CONFIG["SCAN_INTERVAL"])

        except Exception as e:

            log.error(f"Error: {e}")

            time.sleep(30)


if __name__ == "__main__":
    run()