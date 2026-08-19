import pandas as pd

class InternalizationEngine:
    def __init__(self, ledger):
        self.ledger = ledger
        
    def calculate_net_exposure(self):
        if self.ledger.empty:
            return pd.DataFrame(), 0.0
            
        net_pos = self.ledger.groupby(['Ticker', 'AssetClass', 'Jurisdiction']).agg({
            'Quantity': 'sum',
            'Notional': 'sum'
        }).reset_index()
        
        gross_total = self.ledger['Quantity'].abs().sum()
        net_total = net_pos['Quantity'].abs().sum()
        
        ratio = 1 - (net_total / gross_total) if gross_total > 0 else 0
        return net_pos, ratio
