"""
API-Football 客户端
封装足球数据 API 调用
"""
import requests
from typing import Optional, List, Dict, Any
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
        if not self.api_key:
            # 返回模拟数据（如果没有 API Key）
            return self._mock_data(endpoint, params)
        
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return self._mock_data(endpoint, params)
    
    def _mock_data(self, endpoint: str, params: dict = None) -> dict:
        """返回模拟数据（开发/测试用）"""
        if "live" in endpoint or "fixtures" in endpoint:
            return {
                "response": [
                    {
                        "fixture": {
                            "id": 1,
                            "date": "2026-02-28T20:00:00Z",
                            "status": {"short": "2H"}
                        },
                        "teams": {
                            "home": {"name": "Manchester United", "logo": "..."},
                            "away": {"name": "Liverpool", "logo": "..."}
                        },
                        "goals": {"home": 2, "away": 1},
                        "score": {"halftime": {"home": 1, "away": 1}}
                    },
                    {
                        "fixture": {
                            "id": 2,
                            "date": "2026-02-28T20:00:00Z",
                            "status": {"short": "1H"}
                        },
                        "teams": {
                            "home": {"name": "Barcelona", "logo": "..."},
                            "away": {"name": "Real Madrid", "logo": "..."}
                        },
                        "goals": {"home": 0, "away": 0},
                        "score": {"halftime": {"home": 0, "away": 0}}
                    }
                ]
            }
        elif "statistics" in endpoint:
            return {
                "response": [
                    {
                        "team": {"name": "Manchester United"},
                        "statistics": {
                            "shots": 15,
                            "shotsOnGoal": 8,
                            "possession": 55,
                            "passes": 450,
                            "passAccuracy": 82,
                            "fouls": 10,
                            "corners": 6
                        }
                    }
                ]
            }
        return {"response": []}
    
    # ============ 主要 API 方法 ============
    
    def get_live_matches(self) -> List[Dict[str, Any]]:
        """获取当前进行中的比赛"""
        data = self._request("/fixtures/live", {"league": 39})  # Premier League
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
        data = self._request(
            "/standings",
            {"league": league_id, "season": season}
        )
        return data.get("response", [])
    
    def get_team_stats(self, team_id: int) -> Dict[str, Any]]:
        """获取球队统计"""
        data = self._request("/teams/statistics", {"team": team_id})
        return data.get("response", [])
