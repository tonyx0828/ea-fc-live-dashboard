"""
Stock Screener Module
Based on professional trading strategies from:
- CANSLIM (William O'Neil)
- Momentum/Growth investing
- Value screening
"""
import yfinance as yf
import polars as pl
from datetime import datetime, timedelta
import json

# Famous stock screening strategies
STRATEGIES = {
    "canslim": {
        "name": "CANSLIM",
        "description": "William O'Neil's method - Focus on growth stocks with strong fundamentals",
        "criteria": {
            "C": {"name": "Current Quarterly Earnings", "operator": ">", "value": 25, "unit": "%"},
            "A": {"name": "Annual Earnings Growth", "operator": ">", "value": 25, "unit": "%"},
            "N": {"name": "New Highs", "operator": "near", "value": 52, "unit": "weeks"},
            "S": {"name": "Supply/Demand", "operator": ">", "value": 1.5, "unit": "M shares"},
            "L": {"name": "Leader/Laggard", "operator": ">", "value": 1.0, "unit": "RS rating"},
            "I": {"name": "Institutional Sponsorship", "operator": ">", "value": 2, "unit": "funds"},
            "M": {"name": "Market Direction", "operator": ">", "value": 200, "unit": "SMA"}
        }
    },
    "momentum": {
        "name": "Momentum Growth",
        "description": "Stocks with strong recent performance and high relative strength",
        "criteria": {
            "rsi": {"name": "RSI", "operator": "<", "value": 70, "range": "14 days"},
            "price_change_1m": {"name": "1-Month Change", "operator": ">", "value": 5, "unit": "%"},
            "price_change_3m": {"name": "3-Month Change", "operator": ">", "value": 15, "unit": "%"},
            "volume_ratio": {"name": "Volume Ratio", "operator": ">", "value": 1.2, "unit": "x"},
            "sma_50": {"name": "Above 50-Day MA", "operator": ">", "value": 0, "unit": "price"}
        }
    },
    "value": {
        "name": "Value Investing",
        "description": "Undervalued stocks with strong fundamentals",
        "criteria": {
            "pe_ratio": {"name": "P/E Ratio", "operator": "<", "value": 20, "unit": "x"},
            "pb_ratio": {"name": "P/B Ratio", "operator": "<", "value": 3, "unit": "x"},
            "peg_ratio": {"name": "PEG Ratio", "operator": "<", "value": 1.5, "unit": "x"},
            "dividend_yield": {"name": "Dividend Yield", "operator": ">", "value": 2, "unit": "%"},
            "debt_equity": {"name": "Debt/Equity", "operator": "<", "value": 0.5, "unit": "x"}
        }
    },
    "oversold": {
        "name": "Oversold Reversal",
        "description": "Potentially oversold stocks that may bounce back",
        "criteria": {
            "rsi": {"name": "RSI", "operator": "<", "value": 30, "range": "14 days"},
            "rsi_oversold": {"name": "RSI (Strong)", "operator": "<", "value": 25, "range": "14 days"},
            "price_change_1m": {"name": "1-Month Change", "operator": "<", "value": -5, "unit": "%"},
            "volume_ratio": {"name": "Volume", "operator": ">", "value": 0.8, "unit": "x"},
            "sma_200": {"name": "Above 200-Day MA", "operator": ">", "value": 0, "unit": "price"}
        }
    },
    "breakout": {
        "name": "Breakout Candidates",
        "description": "Stocks consolidating near breakout levels",
        "criteria": {
            "price_range_52w": {"name": "52-Week Range", "operator": ">", "value": 0.7, "unit": "%"},
            "volume_ratio": {"name": "Volume Surge", "operator": ">", "value": 1.5, "unit": "x"},
            "sma_50": {"name": "Above 50-Day MA", "operator": ">", "value": 0, "unit": "price"},
            "sma_200": {"name": "Above 200-Day MA", "operator": ">", "value": 0, "unit": "price"},
            "tight_consolidation": {"name": "Tight Range", "operator": "<", "value": 10, "unit": "%"}
        }
    }
}

# Default stock universe (S&P 500 components for demo)
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK.B", "JPM", "JNJ",
    "V", "UNH", "HD", "PG", "MA", "DIS", "PYPL", "NFLX", "ADBE", "CRM",
    "INTC", "CSCO", "PFE", "TMO", "ABT", "NKE", "VZ", "KO", "PEP", "WMT",
    "BA", "IBM", "GE", "MMM", "CAT", "HON", "QCOM", "TXN", "AVGO", "ORCL"
]

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    if len(prices) < period + 1:
        return None
    
    deltas = prices.diff()
    gains = deltas.where(deltas > 0, 0)
    losses = -deltas.where(deltas < 0, 0)
    
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.tail(1).item()

def get_stock_data(ticker, period="3mo"):
    """Get comprehensive stock data"""
    try:
        import yfinance as yf
    except Exception as e:
        print(f"yfinance import error: {e}")
        return {"error": f"yfinance not available: {e}", "ticker": ticker}
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get historical data for calculations
        hist = stock.history(period=period)
        if hist.empty:
            return None
        
        # Calculate indicators
        close = hist['Close']
        volume = hist['Volume']
        
        # RSI
        rsi = calculate_rsi(close, 14)
        
        # Moving averages
        sma_20 = close.rolling(20).mean().tail(1).item()
        sma_50 = close.rolling(50).mean().tail(1).item()
        sma_200 = close.rolling(200).mean().tail(1).item() if len(close) >= 200 else None
        
        # Price changes
        price = close.tail(1).item()
        change_1m = ((price - close.tail(21).head(1).item()) / close.tail(21).head(1).item() * 100) if len(close) >= 21 else 0
        change_3m = ((price - close.tail(63).head(1).item()) / close.tail(63).head(1).item() * 100) if len(close) >= 63 else 0
        
        # Volume
        avg_volume = volume.tail(20).mean()
        current_volume = volume.tail(1).item()
        volume_ratio = current_volume / avg_volume if avg_volume else 1
        
        # 52-week range
        high_52w = hist['High'].tail(252).max()
        low_52w = hist['Low'].tail(252).min()
        price_range_52w = (price - low_52w) / (high_52w - low_52w) * 100 if high_52w != low_52w else 50
        
        # Fundamentals from info
        fundamentals = {
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio"),
            "dividend_yield": info.get("dividendYield"),
            "debt_equity": info.get("debtToEquity"),
            "profit_margin": info.get("profitMargins"),
            "roe": info.get("returnOnEquity"),
            "eps": info.get("trailingEps"),
            "beta": info.get("beta"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "description": info.get("longBusinessSummary", "")[:200]
        }
        
        return {
            "ticker": ticker,
            "name": info.get("shortName", ticker),
            "price": price,
            "change_1m": change_1m,
            "change_3m": change_3m,
            "volume": current_volume,
            "volume_ratio": volume_ratio,
            "rsi": rsi,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "price_range_52w": price_range_52w,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "fundamentals": fundamentals,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def screen_stocks(tickers, strategy="momentum", limit=20):
    """Screen stocks based on strategy"""
    
    print(f"Screening {len(tickers)} stocks with strategy: {strategy}...")
    
    results = []
    for i, ticker in enumerate(tickers):
        print(f"  [{i+1}/{len(tickers)}] Analyzing {ticker}...")
        data = get_stock_data(ticker)
        
        if not data:
            continue
        
        # Handle error response
        if data.get("error"):
            print(f"  Error: {data.get('error')}")
            continue
        
        score = 0
        signals = []
        
        if strategy == "momentum":
            # Momentum strategy scoring
            if data["rsi"] and data["rsi"] < 70:
                score += 2
                signals.append(f"RSI: {data['rsi']:.1f}")
            
            if data["change_1m"] > 5:
                score += 2
                signals.append(f"+1M: {data['change_1m']:.1f}%")
            
            if data["change_3m"] > 15:
                score += 2
                signals.append(f"+3M: {data['change_3m']:.1f}%")
            
            if data["volume_ratio"] > 1.2:
                score += 1
                signals.append(f"Vol: {data['volume_ratio']:.1f}x")
            
            if data["price"] > data["sma_50"]:
                score += 1
                signals.append("> SMA50")
                
        elif strategy == "oversold":
            # Oversold reversal
            if data["rsi"] and data["rsi"] < 30:
                score += 3
                signals.append(f"Oversold RSI: {data['rsi']:.1f}")
            
            if data["change_1m"] < -5:
                score += 2
                signals.append(f"Down: {data['change_1m']:.1f}%")
            
            if data["price"] > data["sma_200"]:
                score += 2
                signals.append("> SMA200")
                
        elif strategy == "value":
            # Value strategy
            pe = data["fundamentals"].get("pe_ratio")
            if pe and 0 < pe < 20:
                score += 2
                signals.append(f"P/E: {pe:.1f}")
            
            peg = data["fundamentals"].get("peg_ratio")
            if peg and 0 < peg < 1.5:
                score += 2
                signals.append(f"PEG: {peg:.1f}")
            
            div = data["fundamentals"].get("dividend_yield")
            if div and div > 2:
                score += 2
                signals.append(f"Div: {div:.1f}%")
                
        elif strategy == "breakout":
            # Breakout candidates
            if data["price_range_52w"] > 70:
                score += 2
                signals.append(f"Near High: {data['price_range_52w']:.0f}%")
            
            if data["volume_ratio"] > 1.5:
                score += 2
                signals.append(f"Vol Surge: {data['volume_ratio']:.1f}x")
            
            if data["price"] > data["sma_50"] and data["price"] > data["sma_200"]:
                score += 2
                signals.append("Bullish MA")
                
        elif strategy == "canslim":
            # CANSLIM (simplified)
            eps = data["fundamentals"].get("eps")
            if eps and eps > 0:
                score += 2
                signals.append(f"EPS: ${eps:.2f}")
            
            if data["price_range_52w"] > 80:
                score += 2
                signals.append("New Highs")
            
            if data["volume_ratio"] > 1.5:
                score += 1
                signals.append("Strong Volume")
            
            if data["price"] > data["sma_50"]:
                score += 1
                signals.append("Above SMA50")
        
        if score > 0:
            data["score"] = score
            data["signals"] = signals
            results.append(data)
    
    # Sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    return results[:limit]

def get_market_summary():
    """Get overall market data"""
    try:
        # Major indices
        indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ"
        }
        
        summary = {}
        for symbol, name in indices.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            
            if not hist.empty:
                current = hist['Close'].tail(1).item()
                prev = hist['Close'].head(1).item()
                change = ((current - prev) / prev) * 100
                
                summary[name] = {
                    "price": current,
                    "change": change
                }
        
        return summary
    except Exception as e:
        print(f"Error fetching market: {e}")
        return {}

if __name__ == "__main__":
    # Test
    print("Testing stock screener...")
    results = screen_stocks(DEFAULT_TICKERS[:10], "momentum")
    print(f"\nFound {len(results)} stocks")
    for r in results[:5]:
        print(f"  {r['ticker']}: {r['name']} - Score: {r['score']}")
