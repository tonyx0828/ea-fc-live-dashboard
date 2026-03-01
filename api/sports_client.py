"""
Multi-Sport Live Dashboard API Client
"""
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime
from config import settings


# All sports with their API endpoints
SPORTS = {
    "basketball": {
        "name": "Basketball",
        "base_url": "https://v1.basketball.api-sports.io",
        "emoji": "🏀",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "nba": {
        "name": "NBA",
        "base_url": "https://v2.nba.api-sports.io",
        "emoji": "🏀",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "nfl": {
        "name": "NFL",
        "base_url": "https://v1.american-football.api-sports.io",
        "emoji": "🏈",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "afl": {
        "name": "AFL",
        "base_url": "https://v1.afl.api-sports.io",
        "emoji": "🏉",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "hockey": {
        "name": "Hockey",
        "base_url": "https://v1.hockey.api-sports.io",
        "emoji": "🏒",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "baseball": {
        "name": "Baseball",
        "base_url": "https://v1.baseball.api-sports.io",
        "emoji": "⚾",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "handball": {
        "name": "Handball",
        "base_url": "https://v1.handball.api-sports.io",
        "emoji": "🤾",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "formula1": {
        "name": "Formula 1",
        "base_url": "https://v1.formula-1.api-sports.io",
        "emoji": "🏎️",
        "endpoint": "/races",
        "params": {"tab": "scheduled"}
    },
    "mma": {
        "name": "MMA",
        "base_url": "https://v1.mma.api-sports.io",
        "emoji": "🥊",
        "endpoint": "/fights",
        "params": {"tab": "scheduled"}
    },
    "rugby": {
        "name": "Rugby",
        "base_url": "https://v1.rugby.api-sports.io",
        "emoji": "🏉",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    },
    "volleyball": {
        "name": "Volleyball",
        "base_url": "https://v1.volleyball.api-sports.io",
        "emoji": "🏐",
        "endpoint": "/fixtures",
        "params": {"date": datetime.now().strftime("%Y-%m-%d")}
    }
}


class MultiSportAPIClient:
    """Multi-sport API client"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.API_FOOTBALL_KEY
        self.headers = {
            "x-apisports-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _request(self, base_url: str, endpoint: str, params: dict = None) -> dict:
        """Send API request to specific sport API"""
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params or {}, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Request error: {e}")
        return {"response": []}
    
    def get_all_live_matches(self) -> Dict[str, List]:
        """Get matches for all available sports"""
        result = {}
        today = datetime.now().strftime("%Y-%m-%d")
        
        if not self.api_key or self.api_key == "demo_key":
            return {"message": {"name": "No API Key", "emoji": "🔑", "count": 0, "matches": []}}
        
        # Try each sport
        for sport_key, sport_info in SPORTS.items():
            try:
                # Build params - use today's date for fixtures
                params = sport_info["params"].copy()
                if sport_info["endpoint"] == "/fixtures":
                    params["date"] = today
                
                data = self._request(sport_info["base_url"], sport_info["endpoint"], params)
                
                matches = data.get("response", [])
                if matches:
                    result[sport_key] = {
                        "name": sport_info["name"],
                        "emoji": sport_info["emoji"],
                        "count": len(matches),
                        "matches": matches
                    }
                    print(f"✅ {sport_key}: {len(matches)} matches")
                else:
                    print(f"⚪ {sport_key}: 0 matches")
                    
            except Exception as e:
                print(f"❌ {sport_key}: {e}")
        
        if not result:
            result["message"] = {
                "name": "No Matches",
                "emoji": "😴",
                "count": 0,
                "matches": [],
                "note": "No matches today!"
            }
        
        return result
    
    def get_live_matches(self, sport: str = "basketball") -> List[Dict[str, Any]]:
        """Get matches for a specific sport"""
        if sport not in SPORTS:
            return []
        
        sport_info = SPORTS[sport]
        params = sport_info["params"].copy()
        if sport_info["endpoint"] == "/fixtures":
            params["date"] = datetime.now().strftime("%Y-%m-%d")
        
        data = self._request(sport_info["base_url"], sport_info["endpoint"], params)
        
        return data.get("response", [])
