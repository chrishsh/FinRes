import numpy as np
import pandas as pd
from scipy.optimize import linprog

class CollateralOptimizer:
    def __init__(self, long_inventory, margin_reqs):
        """
        long_inventory: dict {ticker: notional_value}
        margin_reqs: dict {counterparty: margin_req}
        """
        self.inventory = long_inventory
        self.margin_reqs = margin_reqs
        
        self.haircuts = {t: 0.02 if t in ['AGG', 'TLT'] else 0.10 for t in self.inventory.keys()}
        # Cost to pledge: Keep HQLA (Bonds), pledge Equities
        self.cost = {t: 0.05 if t in ['AGG', 'TLT'] else 0.01 for t in self.inventory.keys()}
        
    def optimize(self):
        tickers = list(self.inventory.keys())
        reqs = list(self.margin_reqs.keys())
        
        if not tickers or not reqs:
            return pd.DataFrame(), False
            
        num_t = len(tickers)
        num_r = len(reqs)
        
        c = np.zeros(num_t * num_r)
        for i in range(num_t):
            for j in range(num_r):
                c[i * num_r + j] = self.cost[tickers[i]]
                
        # Supply Constraint
        A_ub = np.zeros((num_t, num_t * num_r))
        b_ub = np.zeros(num_t)
        for i in range(num_t):
            for j in range(num_r):
                A_ub[i, i * num_r + j] = 1
            b_ub[i] = self.inventory[tickers[i]]
            
        # Demand Constraint
        A_req = np.zeros((num_r, num_t * num_r))
        b_req = np.zeros(num_r)
        for j in range(num_r):
            for i in range(num_t):
                A_req[j, i * num_r + j] = -(1 - self.haircuts[tickers[i]])
            b_req[j] = -self.margin_reqs[reqs[j]]
            
        A_ub = np.vstack((A_ub, A_req))
        b_ub = np.concatenate((b_ub, b_req))
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')
        
        allocations = []
        if res.success:
            x = res.x.reshape((num_t, num_r))
            for i, t in enumerate(tickers):
                for j, r in enumerate(reqs):
                    if x[i,j] > 0.01:
                        allocations.append({
                            'Ticker': t,
                            'Counterparty': r,
                            'Allocated_Notional': x[i,j],
                            'Haircut': self.haircuts[t],
                            'Effective_Margin': x[i,j] * (1 - self.haircuts[t])
                        })
        return pd.DataFrame(allocations), res.success
