import numpy as np

class SecurityLocateEngine:
    def __init__(self, tickers):
        self.rates = {}
        np.random.seed(101)
        for t in tickers:
            self.rates[t] = np.random.uniform(0.0025, 0.01) # GC rates
        # Mock HTB
        if 'AAPL' in self.rates:
            self.rates['AAPL'] = 0.065 # 6.5% HTB
            
    def get_locate(self, ticker, quantity):
        # Mocks a PB API response
        rate = self.rates.get(ticker, 0.01)
        locate_id = np.random.randint(100000, 999999)
        return {
            'Locate_ID': locate_id,
            'Borrow_Fee_Rate': rate,
            'Secured': True
        }
