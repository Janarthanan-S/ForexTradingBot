
import MetaTrader5 as mt5

class ExecutionEngine:

    @staticmethod
    def place_trade(symbol, direction, lot, sl, tp):

        tick = mt5.symbol_info_tick(symbol)

        price = tick.ask if direction=="BUY" else tick.bid

        order_type = mt5.ORDER_TYPE_BUY if direction=="BUY" else mt5.ORDER_TYPE_SELL

        request = {

            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation":10,
            "magic":20260316

        }

        return mt5.order_send(request)
