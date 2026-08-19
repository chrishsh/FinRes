from src.inventory import InventoryManager
from src.internalization import InternalizationEngine
from src.locates import SecurityLocateEngine
from src.compliance import RegulatoryComplianceEngine
from src.optimizer import CollateralOptimizer
from src.pnl import PnLEngine

def run_automated_pipeline():
    print("Starting Automated Portfolio Financing Pipeline...\n")
    
    # 1. Inventory & Data
    tickers = ['AAPL', 'MSFT', 'JPM', 'AGG', 'TLT', '0700.HK']
    strategies = ['StatArb', 'VolArb', 'Macro']
    
    inventory_mgr = InventoryManager(tickers, strategies)
    inventory_mgr.fetch_market_data()
    ledger = inventory_mgr.generate_mock_inventory()
    print("1. Gross Inventory Loaded.")
    
    # 2. Internalization
    int_engine = InternalizationEngine(ledger)
    net_exposure, int_ratio = int_engine.calculate_net_exposure()
    print(f"2. Internalization Complete. Netting Ratio: {int_ratio*100:.2f}%")
    
    # 3. Compliance & Locates
    locate_engine = SecurityLocateEngine(tickers)
    comp_engine = RegulatoryComplianceEngine(locate_engine)
    validated_exposure = comp_engine.validate_exposure(net_exposure)
    print("3. Compliance Checks & Locates Secured.")
    
    # 4. Collateral Optimization
    longs = validated_exposure[(validated_exposure['Quantity'] > 0) & (validated_exposure['Compliance_Status'] == 'Passed')]
    long_inv = longs.groupby('Ticker')['Notional'].sum().to_dict()
    margin_reqs = {'PrimeBroker_A': 1500000, 'ClearingHouse_B': 500000}
    
    optimizer = CollateralOptimizer(long_inv, margin_reqs)
    alloc_df, opt_success = optimizer.optimize()
    print(f"4. Collateral Optimization: {'Success' if opt_success else 'Failed'}")
    
    # 5. P&L Engine
    pnl_engine = PnLEngine(inventory_mgr.prices)
    pnl_df, total_pnl = pnl_engine.calculate_automated_pnl(validated_exposure)
    print(f"5. Daily P&L Calculation Complete. Total Daily Financing Cost: ${total_pnl:.2f}\n")
    
    print("Pipeline Execution Finished.")

if __name__ == "__main__":
    run_automated_pipeline()
