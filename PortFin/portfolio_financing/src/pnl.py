import pandas as pd

class PnLEngine:
    def __init__(self, prices, benchmark_rate=0.05):
        self.prices = prices
        self.benchmark_rate = benchmark_rate
        
    def calculate_automated_pnl(self, validated_exposure):
        pnl_records = []
        total = 0.0
        
        if validated_exposure.empty:
            return pd.DataFrame(), 0.0
            
        for _, row in validated_exposure.iterrows():
            if row['Compliance_Status'] != 'Passed':
                continue
                
            qty = row['Quantity']
            notional = abs(qty * self.prices.get(row['Ticker'], 100))
            
            if qty < 0: # Short borrow fee
                rate = row.get('Borrow_Fee_Rate', 0.01)
                cost = -(notional * rate) / 360
                total += cost
                pnl_records.append({'Ticker': row['Ticker'], 'Type': 'Automated Short Borrow', 'Daily_PnL': cost})
            elif qty > 0: # Long financing
                rate = self.benchmark_rate
                cost = -(notional * rate) / 360
                total += cost
                pnl_records.append({'Ticker': row['Ticker'], 'Type': 'Automated Long Financing', 'Daily_PnL': cost})
                
        return pd.DataFrame(pnl_records), total
        
    def calculate_manual_pnl(self, manual_blotter, simulated_price_change=0.0):
        pnl_records = []
        total = 0.0
        
        if manual_blotter.empty:
            return pd.DataFrame(), 0.0
            
        for _, row in manual_blotter.iterrows():
            trade_type = row['Type']
            pnl = 0.0
            
            if trade_type == 'Repo':
                pnl = -(row['Notional'] * row['Rate']) / 360
            elif trade_type == 'Reverse Repo':
                pnl = (row['Notional'] * row['Rate']) / 360
                
            elif trade_type == 'TRS' or trade_type == 'Equity Swap':
                fin_rate = self.benchmark_rate + row['Rate']
                fin_cost = -(row['Notional'] * fin_rate) / 360
                
                perf = row.get('Quantity', 0) * simulated_price_change
                if row.get('Direction') == 'Pay':
                    perf = -perf
                pnl = fin_cost + perf
                
            elif trade_type == 'Securities Borrow':
                pnl = -(row['Notional'] * row['Rate']) / 360
            elif trade_type == 'Securities Loan':
                pnl = (row['Notional'] * row['Rate']) / 360
                
            elif trade_type == 'Cash Borrow':
                pnl = -(row['Notional'] * row['Rate']) / 360
            elif trade_type == 'Cash Lend':
                pnl = (row['Notional'] * row['Rate']) / 360
                
            elif trade_type == 'Sell Buyback':
                implied_rate = (row['Forward_Price'] - row['Spot_Price']) / row['Spot_Price']
                pnl = -(row['Notional'] * implied_rate) / 360
                
            total += pnl
            pnl_records.append({'Trade_ID': row['Trade_ID'], 'Ticker': row['Ticker'], 'Type': trade_type, 'Daily_PnL': pnl})
                
        return pd.DataFrame(pnl_records), total
