"""
REST API 路由
"""
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from api.football_client import FootballAPIClient
from api.sports_client import MultiSportAPIClient
from processing.polars_processor import MatchAnalyzer
from config import settings


router = APIRouter()

# 初始化组件
football_client = FootballAPIClient(settings.API_FOOTBALL_KEY)
sports_client = MultiSportAPIClient(settings.API_FOOTBALL_KEY)
match_analyzer = MatchAnalyzer()


# ============ 响应模型 ============

class MatchResponse(BaseModel):
    id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str


class StatsResponse(BaseModel):
    match_id: int
    analysis: dict


# ============ 路由 ============

@router.get("/leagues")
async def get_leagues():
    """
    获取可用联赛列表
    """
    leagues = football_client.get_leagues()
    return {
        "count": len(leagues),
        "data": leagues[:10]  # 返回前10个
    }


@router.get("/matches/live")
async def get_live_matches(
    league: Optional[int] = Query(None, description="联赛ID")
):
    """
    获取当前进行中的比赛
    """
    matches = football_client.get_live_matches()
    
    # 用 Polars 格式化数据
    formatted = []
    for match in matches:
        home = match.get("teams", {}).get("home", {})
        away = match.get("teams", {}).get("away", {})
        venue = match.get("fixture", {}).get("venue", {})
        status = match.get("fixture", {}).get("status", {})
        
        formatted.append({
            "id": match.get("fixture", {}).get("id"),
            "league_name": match.get("league", {}).get("name", "Premier League"),
            "league_country": match.get("league", {}).get("country", "England"),
            "home_team": home.get("name", "TBD"),
            "home_city": home.get("city", ""),
            "home_stadium": home.get("stadium", ""),
            "away_team": away.get("name", "TBD"),
            "away_city": away.get("city", ""),
            "away_stadium": away.get("stadium", ""),
            "venue": venue.get("name", ""),
            "venue_city": venue.get("city", ""),
            "home_score": match.get("goals", {}).get("home", 0),
            "away_score": match.get("goals", {}).get("away", 0),
            "status": status.get("short", "NS"),
            "status_long": status.get("long", "Not Started"),
            "elapsed": status.get("elapsed", 0),
            "time": match.get("fixture", {}).get("date")
        })
    
    return {
        "count": len(formatted),
        "matches": formatted
    }


@router.get("/matches/{match_id}")
async def get_match(match_id: int):
    """
    获取特定比赛详情
    """
    # 这里简化处理，实际应该调用专门的 API
    matches = football_client.get_live_matches()
    
    for match in matches:
        if match.get("fixture", {}).get("id") == match_id:
            return match
    
    raise HTTPException(status_code=404, detail="Match not found")


@router.get("/stats/{match_id}")
async def get_match_stats(match_id: int):
    """
    获取比赛统计数据 (Polars 处理)
    """
    stats = football_client.get_match_stats(match_id)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    # 用 Polars 分析
    analysis = match_analyzer.analyze_match_stats(stats)
    
    return {
        "match_id": match_id,
        "raw_stats": stats,
        "analysis": analysis
    }


@router.get("/predictions/{match_id}")
async def get_predictions(match_id: int):
    """
    比赛预测 (Polars 数据分析)
    """
    stats = football_client.get_match_stats(match_id)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # 用 Polars 做预测分析
    prediction = match_analyzer.predict_outcome(stats)
    
    return {
        "match_id": match_id,
        "prediction": prediction,
        "model": "polars_analysis_v1"
    }


@router.get("/compare/{team1_id}/{team2_id}")
async def compare_teams(team1_id: int, team2_id: int):
    """
    对比两队历史战绩 (Polars 聚合分析)
    """
    # 获取两队统计
    team1_stats = football_client.get_team_stats(team1_id)
    team2_stats = football_client.get_team_stats(team2_id)
    
    if not team1_stats or not team2_stats:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # 用 Polars 对比分析
    comparison = match_analyzer.compare_teams([team1_stats, team2_stats])
    
    return {
        "team1": team1_stats.get("team", {}).get("name"),
        "team2": team2_stats.get("team", {}).get("name"),
        "comparison": comparison
    }


# ============ Multi-Sport Endpoints ============

@router.get("/sports/live")
async def get_all_sports_live():
    """
    Get live matches for all available sports
    Returns matches from Football, NBA, NFL, NHL, etc.
    """
    all_matches = sports_client.get_all_live_matches()
    
    total_matches = sum(sport["count"] for sport in all_matches.values())
    
    return {
        "total_matches": total_matches,
        "sports": all_matches
    }


@router.get("/sports/{sport}/live")
async def get_sport_live(sport: str):
    """
    Get live matches for a specific sport
    
    Available sports:
    - football (soccer)
    - nba (basketball)
    - nfl (american football)
    - hockey (ice hockey)
    """
    valid_sports = ["football", "nba", "nfl", "hockey"]
    
    if sport.lower() not in valid_sports:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid sport. Available: {', '.join(valid_sports)}"
        )
    
    matches = sports_client.get_live_matches(sport.lower())
    
    return {
        "sport": sport.lower(),
        "count": len(matches),
        "matches": matches
    }
