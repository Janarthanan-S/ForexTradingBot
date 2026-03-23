import MetaTrader5 as mt5

class RiskGuard:

    start_balance = None

    @staticmethod
    def initialize():
        account = mt5.account_info()
        RiskGuard.start_balance = account.balance

    @staticmethod
    def daily_loss_exceeded(max_loss_percent=0.03):

        account = mt5.account_info()

        current_balance = account.balance

        loss = (RiskGuard.start_balance - current_balance) / RiskGuard.start_balance

        if loss >= max_loss_percent:
            return True

        return False