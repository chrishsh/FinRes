import streamlit as st
import sys
import os

# Add parent to path to import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inventory import InventoryManager
from src.internalization import InternalizationEngine
from src.locates import SecurityLocateEngine
from src.compliance import RegulatoryComplianceEngine
from src.optimizer import CollateralOptimizer
from src.pnl import PnLEngine
from src.manual_trades import ManualTradeEntry

st.set_page_config(page_title="Portfolio Financing Suite", layout="wide")

@st.cache_resource
def init_system():
    tickers = ['AAPL', 'MSFT', 'JPM', 'AGG', 'TLT', '0700.HK']
    strategies = ['StatArb', 'VolArb', 'Macro']
    
    inv_mgr = InventoryManager(tickers, strategies)
    inv_mgr.fetch_market_data()
    ledger = inv_mgr.generate_mock_inventory()
    
    int_engine = InternalizationEngine(ledger)
    net_exposure, ratio = int_engine.calculate_net_exposure()
    
    locate_engine = SecurityLocateEngine(tickers)
    comp_engine = RegulatoryComplianceEngine(locate_engine)
    validated = comp_engine.validate_exposure(net_exposure)
    
    manual_trades = ManualTradeEntry()
    pnl_engine = PnLEngine(inv_mgr.prices)
    
    return inv_mgr, ledger, net_exposure, ratio, validated, manual_trades, pnl_engine

inv_mgr, ledger, net_exposure, ratio, validated, manual_trades, pnl_engine = init_system()

st.title("Automated Portfolio Financing System")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory & Internalization", "Compliance & Locates", "Collateral Optimizer", "Manual Trades", "Pricing & P&L"])

with tab1:
    st.header("Internalization Engine")
    st.metric("Internalization Ratio", f"{ratio*100:.2f}%")
    st.subheader("Net External Exposure")
    st.dataframe(net_exposure)
    
with tab2:
    st.header("Regulatory & Compliance Engine")
    st.dataframe(validated)
    
with tab3:
    st.header("Collateral Optimization (MILP)")
    longs = validated[(validated['Quantity'] > 0) & (validated['Compliance_Status'] == 'Passed')]
    long_inv = longs.groupby('Ticker')['Notional'].sum().to_dict()
    margin_reqs = {'PrimeBroker_A': 1500000, 'ClearingHouse_B': 500000}
    
    st.write("Available Long Inventory:", long_inv)
    st.write("Margin Requirements:", margin_reqs)
    
    if st.button("Run Optimizer"):
        opt = CollateralOptimizer(long_inv, margin_reqs)
        alloc, success = opt.optimize()
        if success:
            st.success("Optimization Successful! Cheapest-to-deliver assets pledged.")
            st.dataframe(alloc)
        else:
            st.error("Optimization Failed. Not enough eligible collateral.")
            
with tab4:
    st.header("Manual Trade Entry")
    
    trade_options = [
        "Repo", "Reverse Repo", 
        "Total Return Swap (TRS)", "Equity Swap",
        "Securities Borrowing", "Securities Lending",
        "Cash Borrowing", "Cash Lending",
        "Bond Sell Buyback"
    ]
    trade_type = st.selectbox("Instrument Type", trade_options)
    
    if trade_type in ["Repo", "Reverse Repo"]:
        col1, col2, col3 = st.columns(3)
        ticker = col1.text_input("Collateral Ticker", "AGG")
        principal = col2.number_input("Cash Principal", value=5000000)
        rate = col3.number_input("Repo Rate", value=0.0525, format="%.4f")
        
        if st.button(f"Book {trade_type}"):
            manual_trades.book_repo(ticker, principal, rate, direction=trade_type)
            st.success(f"{trade_type} Booked")
            
    elif trade_type in ["Total Return Swap (TRS)", "Equity Swap"]:
        col1, col2, col3, col4, col5 = st.columns(5)
        ticker = col1.text_input("Underlying Ticker", "AAPL")
        qty = col2.number_input("Quantity", value=10000)
        price = col3.number_input("Spot Price", value=150.0)
        direction = col4.selectbox("Direction", ["Receive", "Pay"])
        spread = col5.number_input("Financing Spread", value=0.005, format="%.4f")
        
        if st.button(f"Book {trade_type}"):
            manual_trades.book_trs(ticker, qty, price, direction, spread)
            st.success(f"{trade_type} Booked")
            
    elif trade_type in ["Securities Borrowing", "Securities Lending"]:
        direction = "Borrow" if "Borrow" in trade_type else "Loan"
        col1, col2, col3, col4 = st.columns(4)
        ticker = col1.text_input("Ticker", "AAPL")
        qty = col2.number_input("Quantity", value=5000)
        price = col3.number_input("Spot Price", value=150.0)
        rate = col4.number_input("Fee/Rebate Rate", value=0.01, format="%.4f")
        
        if st.button(f"Book {trade_type}"):
            manual_trades.book_sec_borrow_loan(ticker, qty, price, rate, direction=direction)
            st.success(f"{trade_type} Booked")
            
    elif trade_type in ["Cash Borrowing", "Cash Lending"]:
        direction = "Borrow" if "Borrow" in trade_type else "Lend"
        col1, col2 = st.columns(2)
        principal = col1.number_input("Principal Amount (USD)", value=1000000)
        rate = col2.number_input("Interest Rate", value=0.05, format="%.4f")
        
        if st.button(f"Book {trade_type}"):
            manual_trades.book_cash_financing(principal, rate, direction=direction)
            st.success(f"{trade_type} Booked")
            
    elif trade_type == "Bond Sell Buyback":
        col1, col2, col3, col4 = st.columns(4)
        ticker = col1.text_input("Bond Ticker", "TLT")
        notional = col2.number_input("Notional", value=1000000)
        spot = col3.number_input("Spot Price", value=98.50)
        fwd = col4.number_input("Forward Price", value=99.00)
        
        if st.button("Book Sell Buyback"):
            manual_trades.book_sell_buyback(ticker, notional, spot, fwd)
            st.success("Sell Buyback Booked")
            
    st.subheader("Trade Blotter")
    blotter = manual_trades.get_blotter()
    st.dataframe(blotter)

with tab5:
    st.header("Pricing & P&L Engine")
    st.write("Calculates daily accruals utilizing Actual/360 convention.")
    
    auto_pnl, auto_total = pnl_engine.calculate_automated_pnl(validated)
    manual_pnl, man_total = pnl_engine.calculate_manual_pnl(manual_trades.get_blotter(), simulated_price_change=5.0)
    
    st.subheader(f"Total Daily Financing Impact: ${auto_total + man_total:,.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Automated Pipeline P&L")
        st.dataframe(auto_pnl)
    with col2:
        st.write("Manual Trades P&L")
        st.dataframe(manual_pnl)
