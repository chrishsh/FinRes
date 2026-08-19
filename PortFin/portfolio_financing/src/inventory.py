import pandas as pd
import yfinance as yf
import numpy as np

class InventoryManager:
    def __init__(self, tickers, strategies):
        self.tickers = tickers
        self.strategies = strategies
        self.prices = {}
        self.ledger = pd.DataFrame()
        
    def fetch_market_data(self):
        for t in self.tickers:
            try:
                dat = yf.Ticker(t).history(period='1d')
                self.prices[t] = dat['Close'].iloc[-1] if not dat.empty else 100.0
            except:
                self.prices[t] = 100.0
                
    def generate_mock_inventory(self):
        records = []
        np.random.seed(42) # Consistent mock
        for strat in self.strategies:
            for t in self.tickers:
                qty = np.random.randint(-10000, 10000)
                if qty != 0:
                    records.append({
                        'Strategy': strat,
                        'Ticker': t,
                        'AssetClass': 'FixedIncome' if t in ['AGG', 'TLT'] else 'Equity',
                        'Jurisdiction': 'APAC' if '.HK' in t or '.T' in t else 'US',
                        'Quantity': qty,
                        'MtM_Price': self.prices.get(t, 100.0),
                        'Notional': qty * self.prices.get(t, 100.0)
                    })
        self.ledger = pd.DataFrame(records)
        return self.ledger
