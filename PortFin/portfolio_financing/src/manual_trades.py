import pandas as pd
from datetime import datetime

class ManualTradeEntry:
    def __init__(self):
        self.trades = []
        
    def _add_trade(self, trade_dict):
        trade_dict['Trade_ID'] = f"M-{len(self.trades)+1}"
        trade_dict['Timestamp'] = datetime.now().isoformat()
        self.trades.append(trade_dict)
        
    def book_repo(self, collateral_ticker, cash_principal, rate, direction="Repo"):
        self._add_trade({
            'Type': direction,
            'Ticker': collateral_ticker,
            'Notional': cash_principal,
            'Rate': rate
        })
        
    def book_trs(self, ticker, quantity, price, direction, spread):
        self._add_trade({
            'Type': 'TRS',
            'Ticker': ticker,
            'Quantity': quantity,
            'Spot_Price': price,
            'Notional': quantity * price,
            'Direction': direction,
            'Rate': spread
        })
        
    def book_sec_borrow_loan(self, ticker, quantity, price, rate, direction):
        self._add_trade({
            'Type': f'Securities {direction}',
            'Ticker': ticker,
            'Quantity': quantity,
            'Spot_Price': price,
            'Notional': quantity * price,
            'Rate': rate
        })
        
    def book_cash_financing(self, principal, rate, direction):
        self._add_trade({
            'Type': f'Cash {direction}',
            'Ticker': 'USD',
            'Notional': principal,
            'Rate': rate
        })
        
    def book_sell_buyback(self, ticker, notional, spot_price, forward_price):
        self._add_trade({
            'Type': 'Sell Buyback',
            'Ticker': ticker,
            'Notional': notional,
            'Spot_Price': spot_price,
            'Forward_Price': forward_price,
            'Rate': 0.0 # Implied rate used in PnL
        })
        
    def get_blotter(self):
        if not self.trades:
            return pd.DataFrame(columns=['Trade_ID', 'Type', 'Ticker', 'Notional', 'Rate', 'Timestamp'])
        return pd.DataFrame(self.trades)
