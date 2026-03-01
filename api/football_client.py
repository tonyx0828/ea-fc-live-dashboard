"""
API-Football 客户端 - 增强版
更真实的模拟数据
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
        """返回模拟数据 - 更真实"""
        # 真实的联赛和球队 + 主场球场
        leagues_teams = [
            {
                "league_id": 39,
                "league": "Premier League",
                "country": "England",
                "teams": [
                    ("Manchester United", "Old Trafford", "Manchester"),
                    ("Liverpool", "Anfield", "Liverpool"),
                    ("Arsenal", "Emirates Stadium", "London"),
                    ("Chelsea", "Stamford Bridge", "London"),
                    ("Manchester City", "Etihad Stadium", "Manchester"),
                    ("Tottenham Hotspur", "Tottenham Hotspur Stadium", "London"),
                    ("Newcastle United", "St James' Park", "Newcastle"),
                    ("Aston Villa", "Villa Park", "Birmingham"),
                ]
            },
            {
                "league_id": 140,
                "league": "La Liga",
                "country": "Spain",
                "teams": [
                    ("Barcelona", "Camp Nou", "Barcelona"),
                    ("Real Madrid", "Santiago Bernabeu", "Madrid"),
                    ("Atletico Madrid", "Metropolitano", "Madrid"),
                    ("Sevilla", "Ramón Sánchez-Pizjuán", "Seville"),
                ]
            },
            {
                "league_id": 78,
                "league": "Bundesliga",
                "country": "Germany",
                "teams": [
                    ("Bayern Munich", "Allianz Arena", "Munich"),
                    ("Borussia Dortmund", "Signal Iduna Park", "Dortmund"),
                    ("RB Leipzig", "Red Bull Arena", "Leipzig"),
                    ("Bayer Leverkusen", "BayArena", "Leverkusen"),
                ]
            },
            {
                "league_id": 135,
                "league": "Serie A",
                "country": "Italy",
                "teams": [
                    ("Juventus", "Allianz Stadium", "Turin"),
                    ("AC Milan", "San Siro", "Milan"),
                    ("Inter Milan", "San Siro", "Milan"),
                    ("Napoli", "Stadio Diego Armando Maradona", "Naples"),
                    ("AS Roma", "Stadio Olimpico", "Rome"),
                ]
            },
            {
                "league_id": 61,
                "league": "Ligue 1",
                "country": "France",
                "teams": [
                    ("Paris Saint-Germain", "Parc des Princes", "Paris"),
                    ("Marseille", "Stade Vélodrome", "Marseille"),
                    ("Lyon", "Groupama Stadium", "Lyon"),
                    ("Monaco", "Stade Louis II", "Monaco"),
                ]
            }
        ]
        
        live_statuses = [
            ("1H", "1st Half"),
            ("HT", "Halftime"),
            ("2H", "2nd Half"),
            ("ET", "Extra Time")
        ]
        
        live_matches = []
        
        # 生成 6-8 场随机比赛
        num_matches = random.randint(6, 8)
        
        for i in range(num_matches):
            # 随机选择联赛
            league_data = random.choice(leagues_teams)
            teams_list = league_data["teams"]
            
            # 随机选择两队
            home_data = random.choice(teams_list)
            away_data = random.choice([t for t in teams_list if t[0] != home_data[0]])
            
            home_team, home_stadium, home_city = home_data
            away_team, away_stadium, away_city = away_data
            
            # 随机状态和时间
            status_short, status_name = random.choice(live_statuses)
            elapsed = random.randint(1, 75) if status_short != "HT" else 45
            
            # 随机比分
            home_goals = random.randint(0, 3)
            away_goals = random.randint(0, 2)
            
            # 随机时间
            base_time = datetime.now() - timedelta(minutes=random.randint(10, 70))
            
            match = {
                "fixture": {
                    "id": 1000 + i,
                    "date": base_time.isoformat() + "Z",
                    "status": {
                        "short": status_short,
                        "long": status_name,
                        "elapsed": elapsed
                    },
                    "venue": {
                        "name": home_stadium,
                        "city": home_city
                    }
                },
                "league": {
                    "id": league_data["league_id"],
                    "name": league_data["league"],
                    "country": league_data["country"],
                    "season": 2024
                },
                "teams": {
                    "home": {
                        "name": home_team,
                        "city": home_city,
                        "stadium": home_stadium
                    },
                    "away": {
                        "name": away_team,
                        "city": away_city,
                        "stadium": away_stadium
                    }
                },
                "goals": {
                    "home": home_goals,
                    "away": away_goals
                },
                "score": {
                    "halftime": {
                        "home": random.randint(0, 2),
                        "away": random.randint(0, 1)
                    },
                    "fulltime": {
                        "home": home_goals,
                        "away": away_goals
                    }
                }
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
