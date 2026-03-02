"""
Multi-Sport Live Dashboard API Client
Supports: Football, NBA, NFL, NHL, MLB, etc.
"""
import requests
from typing import Optional, List, Dict, Any
import random
from datetime import datetime, timedelta
from config import settings


# Sport configurations
SPORTS = {
    "football": {
        "name": "Football",
        "leagues": [39, 140, 78, 135, 61],  # Premier League, La Liga, Bundesliga, Serie A, Ligue 1
        "emoji": "⚽",
        "api_base": "https://v3.football.api-sports.io"
    },
    "basketball": {
        "name": "Basketball",
        "leagues": [12, 13],  # NBA, EuroLeague
        "emoji": "🏀",
        "api_base": "https://v1.basketball.api-sports.io"
    },
    "nba": {
        "name": "NBA",
        "leagues": [12],
        "emoji": "🏀",
        "api_base": "https://v2.nba.api-sports.io"
    },
    "nfl": {
        "name": "NFL",
        "leagues": [1],
        "emoji": "🏈",
        "api_base": "https://v1.american-football.api-sports.io"
    },
    "hockey": {
        "name": "Hockey",
        "leagues": [57],  # NHL
        "emoji": "🏒",
        "api_base": "https://v1.hockey.api-sports.io"
    },
    "baseball": {
        "name": "Baseball",
        "leagues": [1],  # MLB
        "emoji": "⚾",
        "api_base": "https://v1.baseball.api-sports.io"
    },
    "afl": {
        "name": "AFL",
        "leagues": [1],
        "emoji": "🏉",
        "api_base": "https://v1.afl.api-sports.io"
    },
    "formula1": {
        "name": "Formula 1",
        "leagues": [1],
        "emoji": "🏎️",
        "api_base": "https://v1.formula-1.api-sports.io"
    },
    "handball": {
        "name": "Handball",
        "leagues": [1],
        "emoji": "🤾",
        "api_base": "https://v1.handball.api-sports.io"
    },
    "mma": {
        "name": "MMA",
        "leagues": [1],
        "emoji": "🥊",
        "api_base": "https://v1.mma.api-sports.io"
    },
    "rugby": {
        "name": "Rugby",
        "leagues": [1],
        "emoji": "🏉",
        "api_base": "https://v1.rugby.api-sports.io"
    },
    "volleyball": {
        "name": "Volleyball",
        "leagues": [1],
        "emoji": "🏐",
        "api_base": "https://v1.volleyball.api-sports.io"
    }
}


class MultiSportAPIClient:
    """Multi-sport API client"""
    
    # Use basketball API (key works for this)
    BASE_URL = "https://v1.basketball.api-sports.io"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.API_FOOTBALL_KEY
        self.headers = {
            "x-apisports-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _request(self, endpoint: str, params: dict = None) -> dict:
        """Send API request"""
        if not self.api_key or self.api_key == "demo_key":
            return self._mock_data(endpoint, params)
        
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        
        if response.status_code == 200:
            return response.json()
        else:
            return self._mock_data(endpoint, params)
    
    def _mock_data(self, endpoint: str, params: dict = None) -> dict:
        """Generate realistic mock data for different sports"""
        sport = params.get("sport", "football") if params else "football"
        
        # Different mock data for different sports
        if sport == "nba":
            return self._mock_nba_data()
        elif sport == "nfl":
            return self._mock_nfl_data()
        elif sport == "hockey":
            return self._mock_hockey_data()
        else:
            return self._mock_football_data()
    
    def _mock_football_data(self) -> dict:
        """Mock football/soccer data"""
        leagues = [
            {"id": 39, "name": "Premier League", "country": "England"},
            {"id": 140, "name": "La Liga", "country": "Spain"},
            {"id": 78, "name": "Bundesliga", "country": "Germany"},
            {"id": 135, "name": "Serie A", "country": "Italy"},
            {"id": 61, "name": "Ligue 1", "country": "France"},
        ]
        
        teams = [
            ("Manchester United", "Old Trafford", "Manchester"),
            ("Liverpool", "Anfield", "Liverpool"),
            ("Arsenal", "Emirates Stadium", "London"),
            ("Chelsea", "Stamford Bridge", "London"),
            ("Barcelona", "Camp Nou", "Barcelona"),
            ("Real Madrid", "Santiago Bernabeu", "Madrid"),
            ("Bayern Munich", "Allianz Arena", "Munich"),
            ("Juventus", "Allianz Stadium", "Turin"),
        ]
        
        matches = []
        for i in range(5):
            league = random.choice(leagues)
            home, away = random.sample(teams, 2)
            
            matches.append({
                "sport": "football",
                "league": league,
                "home_team": {"name": home[0], "venue": home[1], "city": home[2]},
                "away_team": {"name": away[0], "venue": away[1], "city": away[2]},
                "home_score": random.randint(0, 3),
                "away_score": random.randint(0, 2),
                "status": random.choice(["1H", "2H", "HT"]),
                "time": random.randint(15, 80),
            })
        
        return {"response": matches}
    
    def _mock_nba_data(self) -> dict:
        """Mock NBA data"""
        teams = [
            ("Los Angeles Lakers", "Crypto.com Arena", "Los Angeles"),
            ("Boston Celtics", "TD Garden", "Boston"),
            ("Golden State Warriors", "Chase Center", "San Francisco"),
            ("Miami Heat", "Kasea Center", "Miami"),
            ("Brooklyn Nets", "Barclays Center", "Brooklyn"),
        ]
        
        matches = []
        for i in range(3):
            home, away = random.sample(teams, 2)
            
            matches.append({
                "sport": "basketball",
                "league": {"id": 12, "name": "NBA", "country": "USA"},
                "home_team": {"name": home[0], "venue": home[1], "city": home[2]},
                "away_team": {"name": away[0], "venue": away[1], "city": away[2]},
                "home_score": random.randint(80, 120),
                "away_score": random.randint(75, 115),
                "status": random.choice(["Q1", "Q2", "Q3", "Q4", "HT"]),
                "time": random.randint(1, 12),
            })
        
        return {"response": matches}
    
    def _mock_nfl_data(self) -> dict:
        """Mock NFL data"""
        teams = [
            ("Kansas City Chiefs", "Arrowhead Stadium", "Kansas City"),
            ("San Francisco 49ers", "Levi's Stadium", "Santa Clara"),
            ("Dallas Cowboys", "AT&T Stadium", "Dallas"),
            ("Buffalo Bills", "Highmark Stadium", "Buffalo"),
        ]
        
        matches = []
        for i in range(2):
            home, away = random.sample(teams, 2)
            
            matches.append({
                "sport": "american-football",
                "league": {"id": 1, "name": "NFL", "country": "USA"},
                "home_team": {"name": home[0], "venue": home[1], "city": home[2]},
                "away_team": {"name": away[0], "venue": away[1], "city": away[2]},
                "home_score": random.randint(7, 35),
                "away_score": random.randint(7, 35),
                "status": random.choice(["Q1", "Q2", "Q3", "Q4", "HT"]),
                "time": random.randint(1, 15),
            })
        
        return {"response": matches}
    
    def _mock_hockey_data(self) -> dict:
        """Mock NHL data"""
        teams = [
            ("Toronto Maple Leafs", "Scotiabank Arena", "Toronto"),
            ("Edmonton Oilers", "Rogers Place", "Edmonton"),
            ("Boston Bruins", "TD Garden", "Boston"),
            ("Los Angeles Kings", "Crypto.com Arena", "Los Angeles"),
        ]
        
        matches = []
        for i in range(2):
            home, away = random.sample(teams, 2)
            
            matches.append({
                "sport": "hockey",
                "league": {"id": 57, "name": "NHL", "country": "USA"},
                "home_team": {"name": home[0], "venue": home[1], "city": home[2]},
                "away_team": {"name": away[0], "venue": away[1], "city": away[2]},
                "home_score": random.randint(1, 6),
                "away_score": random.randint(1, 5),
                "status": random.choice(["P1", "P2", "P3", "HT"]),
                "time": random.randint(1, 20),
            })
        
        return {"response": matches}
    
    def get_live_matches(self, sport: str = "football") -> List[Dict[str, Any]]:
        """Get live matches for a specific sport"""
        params = {"sport": sport}
        
        # Try real API first
        if self.api_key and self.api_key != "demo_key":
            for league_id in SPORTS.get(sport, {}).get("leagues", []):
                try:
                    data = self._request("/fixtures/live", {"league": league_id})
                    if data.get("response"):
                        return data.get("response", [])
                except:
                    pass
        
        # Fallback to mock data
        return self._mock_data("", params).get("response", [])
    
    def get_all_live_matches(self) -> Dict[str, List]:
        """Get live matches for all available sports"""
        result = {}
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Only try if we have a valid API key
        if not self.api_key or self.api_key == "demo_key":
            # Return empty sports list for demo mode
            for sport_key, sport_info in SPORTS.items():
                result[sport_key] = {
                    "name": sport_info["name"],
                    "emoji": sport_info["emoji"],
                    "count": 0,
                    "matches": []
                }
            return result
        
        # Fetch data for each sport
        for sport_key, sport_info in SPORTS.items():
            try:
                base_url = sport_info.get("api_base", "https://v1.basketball.api-sports.io")
                
                # Determine endpoint and params based on sport
                if sport_key in ["basketball", "nba"]:
                    # Basketball uses /games endpoint
                    url = f"{base_url}/games"
                    params = {"date": today}
                elif sport_key in ["football"]:
                    # Football uses /fixtures endpoint (no status filter to get all games)
                    url = f"{base_url}/fixtures"
                    params = {"date": today}
                elif sport_key in ["nfl", "afl", "hockey", "baseball", "formula1", "handball", "mma", "rugby", "volleyball"]:
                    # Other sports - try fixtures
                    url = f"{base_url}/games"
                    params = {"date": today}
                else:
                    url = f"{base_url}/games"
                    params = {"date": today}
                
                # Make API request
                headers = {"x-apisports-key": self.api_key}
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("response", [])
                    
                    # Add sport field to each match
                    for match in matches:
                        match["sport"] = sport_key
                    
                    result[sport_key] = {
                        "name": sport_info["name"],
                        "emoji": sport_info["emoji"],
                        "count": len(matches),
                        "matches": matches
                    }
                    print(f"✅ {sport_key}: {len(matches)} matches")
                else:
                    result[sport_key] = {
                        "name": sport_info["name"],
                        "emoji": sport_info["emoji"],
                        "count": 0,
                        "matches": []
                    }
                    
            except Exception as e:
                print(f"❌ {sport_key}: Error - {e}")
                result[sport_key] = {
                    "name": sport_info["name"],
                    "emoji": sport_info["emoji"],
                    "count": 0,
                    "matches": []
                }
        
        return result
