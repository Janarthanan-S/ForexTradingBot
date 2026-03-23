class RiskEngine:

    @staticmethod
    def calculate_lot(balance, risk_percent, sl_distance, symbol):

        risk_amount = balance * risk_percent

        # Get symbol info
        import MetaTrader5 as mt5
        info = mt5.symbol_info(symbol)

        point = info.point
        pip = point * 10

        # Convert price distance → pips
        sl_pips = sl_distance / pip

        if sl_pips == 0:
            return 0.01

        # Standard lot pip value ≈ $10
        lot = risk_amount / (sl_pips * 10)

        # Clamp lot size
        lot = max(0.01, min(lot, 1.0))  # NEVER exceed 1 lot

        return round(lot, 2)