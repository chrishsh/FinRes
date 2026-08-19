# Portfolio Financing System: Prototype & Full-Blown Product Suite

This document outlines the architecture and implementation plan for the **Automated Portfolio Financing System**, serving as a blueprint for both the interactive Jupyter Notebook prototype and the full-blown Python production suite.

## Goal Description
Build an Automated Portfolio Financing system that functions similarly to an Automated Market Maker (AMM). The system autonomously calculates net exposure, allocates optimal collateral, tracks P&L, simulates market conditions, and ensures **cross-border regulatory compliance**. 

Manual intervention is explicitly supported via a comprehensive **Manual Trade Entry Module**, accommodating a full suite of financing instruments (Equity/Bond Borrowing, Repo, Swaps, Sell/Buybacks, etc.).

## Unified Product Specification
For complete documentation, zoom-in workflow diagrams, mathematical models, and compliance rules covering the entire system, please refer to the master specification:
[**Product Functional & Technical Specification**](file:///Users/chrishsieh/.gemini/antigravity/brain/d2a08686-80fc-42e4-b8fd-0b4030a1f404/product_specification_document.md)

*(Note: The specification document has been heavily verified to ensure 100% integrity across the planned Jupyter Notebook prototype and the full-blown Python suite).*

## Phase 1: Prototype Deliverable (Jupyter Notebook)
The Jupyter notebook will be reconstructed to match the exact mathematical specifications and workflows outlined in the master spec document.
*   **Target**: `portfolio_financing_prototype.ipynb`
*   **Modules Included**:
    1.  `InventoryManager` & `yfinance` API integration.
    2.  `InternalizationEngine`
    3.  `RegulatoryComplianceEngine` (with US & APAC Jurisdiction checks)
    4.  `SecurityLocateEngine`
    5.  `CollateralOptimizer`
    6.  `ManualTradeEntry` (with Repo, TRS, and physical borrowing dropdowns)
    7.  `PnLEngine`
*   **Dashboard**: `ipywidgets` GUI encompassing all 7 modules.

## Phase 2: Full-Blown Product Suite
The full-blown product will be structured as a standalone Python package, fully decoupled from the Jupyter environment.

```text
portfolio_financing/
│
├── main.py                 # The automated pipeline runner (orchestrator)
├── requirements.txt        # Dependencies (pandas, scipy, yfinance, streamlit, pytest)
│
├── src/
│   ├── __init__.py
│   ├── inventory.py        # Manages positions, market data (yfinance)
│   ├── internalization.py  # Internalization mathematical logic
│   ├── compliance.py       # US (Reg T/SHO) & APAC (SFC/FSA/MAS) Rule Engine
│   ├── optimizer.py        # MILP/LP Collateral Optimization engine
│   ├── locates.py          # Borrow rate simulation & Reg SHO locate checks
│   ├── manual_trades.py    # Manual trade booking & blotter management
│   └── pnl.py              # Exact pricing math for Repo, TRS, Borrowing, etc.
│
├── tests/
│   ├── __init__.py
│   └── test_engines.py     # Comprehensive automated test suite (pytest)
│
└── app/
    └── dashboard.py        # Streamlit web application for the UI
```

## User Review Required

> [!IMPORTANT]
> This is the **Final Gate Review**. 
> Please verify that the newly added zoom-in `mermaid` diagrams in the [Product Specification](file:///Users/chrishsieh/.gemini/antigravity/brain/d2a08686-80fc-42e4-b8fd-0b4030a1f404/product_specification_document.md) correctly capture the workflows you desire. 
> Once approved, I will immediately execute the creation of the final prototype notebook and the full-blown product suite!
