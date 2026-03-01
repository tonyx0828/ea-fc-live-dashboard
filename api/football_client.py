"""
API-Football 客户端
封装足球数据 API 调用
"""
import requests
from typing import Optional, List, Dict, Any
import random
from datetime import datetime, timedelta
from config import settings


class FootballAPIClient:
    """足球数据 API 客户端"""
    
    BASE_URL = "https://v3.football.api-sports.io"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.API_FOOTBALL_KEY
        self.headers = {
            "x-apisports-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _request(self, endpoint: str, params: dict = None) -> dict:
        """发送 API 请求"""
        if not self.api_key or self.api_key == "demo_key":
            return self._mock_data(endpoint, params)
        
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code}")
            return self._mock_data(endpoint, params)
    
    def _mock_data(self, endpoint: str, params: dict = None) -> dict:
        """返回模拟数据"""
        leagues = [
            (39, "Premier League"),
            (140, "La Liga"),
            (78, "Bundesliga"),
            (135, "Serie A"),
            (61, "Ligue 1")
        ]
        
        teams = [
            ("Manchester United", "Liverpool"),
            ("Barcelona", "Real Madrid"),
            ("Bayern Munich", "Borussia Dortmund"),
            ("Juventus", "AC Milan"),
            ("PSG", "Marseille"),
            ("Arsenal", "Chelsea"),
            ("Manchester City", "Tottenham"),
        ]
        
        live_statuses = ["1H", "2H", "HT"]
        live_matches = []
        
        for i in range(8):
            league = random.choice(leagues)
            home, away = random.choice(teams)
            status = random.choice(live_statuses)
            home_goals = random.randint(0, 3)
            away_goals = random.randint(0, 2)
            base_time = datetime.now() - timedelta(minutes=random.randint(30, 80))
            
            match = {
                "fixture": {
                    "id": 1000 + i,
                    "date": base_time.isoformat() + "Z",
                    "status": {"short": status, "elapsed": random.randint(15, 75)}
                },
                "league": {
                    "id": league[0],
                    "name": league[1],
                    "season": 2024
                },
                "teams": {
                    "home": {"name": home},
                    "away": {"name": away}
                },
                "goals": {"home": home_goals, "away": away_goals},
                "score": {"halftime": {"home": random.randint(0, 2), "away": random.randint(0, 1)}}
            }
            live_matches.append(match)
        
        return {"response": live_matches}
    
    def get_live_matches(self) -> List[Dict[str, Any]]:
        """获取当前进行中的比赛"""
        data = self._request("/fixtures/live", {"league": 39})
        return data.get("response", [])
    
    def get_match_stats(self, match_id: int) -> Dict[str, Any]:
        """获取比赛统计数据"""
        data = self._request("/fixtures/statistics", {"fixture": match_id})
        return data.get("response", [])
    
    def get_leagues(self) -> List[Dict[str, Any]]:
        """获取可用联赛"""
        data = self._request("/leagues")
        return data.get("response", [])
    
    def get_league_standings(self, league_id: int, season: int = 2024) -> Dict[str, Any]:
        """获取联赛积分榜"""
        data = self._request("/standings", {"league": league_id, "season": season})
        return data.get("response", [])
    
    def get_team_stats(self, team_id: int) -> Dict[str, Any]:
        """获取球队统计"""
        data = self._request("/teams/statistics", {"team": team_id})
        return data.get("response", [])
