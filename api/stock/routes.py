"""
Stock Screener API Routes
"""
from fastapi import APIRouter
from typing import Optional, List
from pydantic import BaseModel
from .screener import screen_stocks, get_market_summary, STRATEGIES, DEFAULT_TICKERS

router = APIRouter(prefix="/api/stock", tags=["stock"])

class ScreenerRequest(BaseModel):
    tickers: Optional[List[str]] = None
    strategy: str = "momentum"
    limit: int = 20

@router.get("/strategies")
async def get_strategies():
    """Get available screening strategies"""
    return {
        "strategies": STRATEGIES,
        "default_tickers": DEFAULT_TICKERS
    }

@router.get("/market")
async def market_summary():
    """Get overall market summary"""
    return get_market_summary()

@router.post("/screen")
async def screen(request: ScreenerRequest):
    """Screen stocks based on criteria"""
    tickers = request.tickers if request.tickers else DEFAULT_TICKERS
    
    results = screen_stocks(
        tickers=tickers,
        strategy=request.strategy,
        limit=request.limit
    )
    
    return {
        "strategy": request.strategy,
        "strategy_info": STRATEGIES.get(request.strategy, {}),
        "count": len(results),
        "results": results
    }

@router.get("/ticker/{symbol}")
async def get_ticker(symbol: str):
    """Get detailed info for a single ticker"""
    from .screener import get_stock_data
    
    data = get_stock_data(symbol.upper())
    
    if not data:
        return {"error": "Ticker not found or no data available"}
    
    return data
