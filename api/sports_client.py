"""
Multi-Sport Live Dashboard API Client
Supports: Football, NBA, NFL, NHL, Baseball, AFL, Handball, Formula-1, MMA, Rugby, Volleyball
"""
import requests
from typing import Optional, List, Dict, Any
import random
from datetime import datetime, timedelta
from config import settings


# All sports with their API endpoints - using /games endpoint (confirmed working)
SPORTS = {
    "basketball": {
        "name": "Basketball",
        "base_url": "https://v1.basketball.api-sports.io",
        "emoji": "🏀"
    },
    "nba": {
        "name": "NBA",
        "base_url": "https://v2.nba.api-sports.io",
        "emoji": "🏀"
    },
    "nfl": {
        "name": "NFL",
        "base_url": "https://v1.american-football.api-sports.io",
        "emoji": "🏈"
    },
    "afl": {
        "name": "AFL",
        "base_url": "https://v1.afl.api-sports.io",
        "emoji": "🏉"
    },
    "hockey": {
        "name": "Hockey",
        "base_url": "https://v1.hockey.api-sports.io",
        "emoji": "🏒"
    },
    "baseball": {
        "name": "Baseball",
        "base_url": "https://v1.baseball.api-sports.io",
        "emoji": "⚾"
    },
    "handball": {
        "name": "Handball",
        "base_url": "https://v1.handball.api-sports.io",
        "emoji": "🤾"
    },
    "formula1": {
        "name": "Formula 1",
        "base_url": "https://v1.formula-1.api-sports.io",
        "emoji": "🏎️"
    },
    "mma": {
        "name": "MMA",
        "base_url": "https://v1.mma.api-sports.io",
        "emoji": "🥊"
    },
    "rugby": {
        "name": "Rugby",
        "base_url": "https://v1.rugby.api-sports.io",
        "emoji": "🏉"
    },
    "volleyball": {
        "name": "Volleyball",
        "base_url": "https://v1.volleyball.api-sports.io",
        "emoji": "🏐"
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
        """Get live matches for all available sports"""
        result = {}
        
        if not self.api_key or self.api_key == "demo_key":
            return {"message": {"name": "No API Key", "emoji": "🔑", "count": 0, "matches": []}}
        
        # Try each sport
        for sport_key, sport_info in SPORTS.items():
            try:
                data = self._request(
                    sport_info["base_url"],
                    "/games",
                    {}
                )
                
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
        
        # If no data, show message
        if not result:
            result["message"] = {
                "name": "No Live Matches",
                "emoji": "😴",
                "count": 0,
                "matches": [],
                "note": "No live matches right now!"
            }
        
        return result
    
    def get_live_matches(self, sport: str = "basketball") -> List[Dict[str, Any]]:
        """Get live matches for a specific sport"""
        if sport not in SPORTS:
            return []
        
        sport_info = SPORTS[sport]
        data = self._request(sport_info["base_url"], "/games", {})
        
        return data.get("response", [])
