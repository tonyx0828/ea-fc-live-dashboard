"""
EA FC Live Dashboard - 高级版
展示 FastAPI + WebSocket + Polars 完整整合
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from typing import Optional, List
import json
from datetime import datetime

from api.football_client import FootballAPIClient
from api.routes import router as api_router
from websocket.manager import ConnectionManager
from processing.polars_processor import MatchAnalyzer
from processing.advanced_analyzer import AdvancedMatchAnalyzer
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("🚀 EA FC Live Dashboard 高级版启动...")
    yield
    print("👋 应用关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="EA FC Live Dashboard",
    description="实时足球数据看板 - 高级版 (Polars + WebSocket)",
    version="2.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务 (前端)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 全局组件
football_client = FootballAPIClient(settings.API_FOOTBALL_KEY)
match_analyzer = MatchAnalyzer()
advanced_analyzer = AdvancedMatchAnalyzer()
ws_manager = ConnectionManager()


# ============ 路由 ============

@app.get("/")
async def root():
    # 优先返回前端页面
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "ok",
        "message": "EA FC Live Dashboard Running",
        "docs": "/docs",
        "frontend": "Open / to view frontend",
        "features": [
            "REST API",
            "WebSocket 实时推送",
            "Polars 高级分析",
            "多维度过滤"
        ]
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "websocket_connections": len(ws_manager.active_connections),
    }


# 挂载 API 路由
app.include_router(api_router, prefix="/api", tags=["Football"])


# ============ 高级过滤 API ============

@app.get("/api/v2/matches/filter")
async def filter_matches(
    league_ids: Optional[str] = Query(None, description="联赛ID, 逗号分隔"),
    team_name: Optional[str] = Query(None, description="球队名称"),
    min_goals: Optional[int] = Query(0, ge=0, le=10, description="最小进球数"),
    max_goals: Optional[int] = Query(10, ge=0, le=20, description="最大进球数"),
    live_only: bool = Query(False, description="只看Live比赛"),
    date_from: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    高级过滤查询 - 展示 Polars 的强大过滤能力
    """
    # 1. 获取数据
    raw_matches = football_client.get_live_matches()
    
    # 2. 用 Polars 加载和处理
    df = advanced_analyzer.load_matches(raw_matches)
    
    # 3. 逐个应用过滤条件 (Polars 优势：链式调用)
    
    if league_ids:
        ids = [int(x.strip()) for x in league_ids.split(",")]
        df = advanced_analyzer.filter_by_league(df, ids)
    
    if team_name:
        df = advanced_analyzer.filter_by_team(df, team_name)
    
    if date_from or date_to:
        df = advanced_analyzer.filter_by_date_range(df, date_from, date_to)
    
    if live_only:
        df = advanced_analyzer.filter_live_only(df)
    
    if min_goals > 0 or max_goals < 10:
        df = advanced_analyzer.filter_by_score_range(df, min_goals, max_goals)
    
    # 4. 限制返回数量
    df = df.head(limit)
    
    return {
        "filters_applied": {
            "league_ids": league_ids,
            "team_name": team_name,
            "min_goals": min_goals,
            "max_goals": max_goals,
            "live_only": live_only,
            "date_range": f"{date_from} to {date_to}" if date_from or date_to else None,
        },
        "total_matches": len(df),
        "matches": df.to_dicts()
    }


@app.get("/api/v2/stats/advanced/{match_id}")
async def advanced_stats(match_id: int):
    """
    高级比赛统计分析
    """
    raw_stats = football_client.get_match_stats(match_id)
    
    # 用高级分析器处理
    if raw_stats:
        # 这里简化处理，实际应该传完整数据
        analysis = advanced_analyzer.calculate_advanced_stats(
            advanced_analyzer.load_matches(raw_stats)
        )
    else:
        analysis = {}
    
    return {
        "match_id": match_id,
        "analysis": analysis,
        "generated_at": datetime.now().isoformat()
    }


@app.get("/api/v2/analytics/form/{team_name}")
async def team_form(
    team_name: str,
    last_n: int = Query(5, ge=1, le=20, description="最近N场")
):
    """
    球队最近状态分析
    """
    raw_matches = football_client.get_live_matches()
    df = advanced_analyzer.load_matches(raw_matches)
    
    form = advanced_analyzer.calculate_team_form(df, team_name, last_n)
    
    return {
        "team": team_name,
        "analysis": form,
        "generated_at": datetime.now().isoformat()
    }


@app.get("/api/v2/analytics/league-table")
async def league_table(
    league_id: int = Query(..., description="联赛ID"),
):
    """
    联赛积分榜计算
    """
    raw_matches = football_client.get_live_matches()
    df = advanced_analyzer.load_matches(raw_matches)
    
    # 过滤联赛
    df = advanced_analyzer.filter_by_league(df, [league_id])
    
    # 计算积分榜
    table = advanced_analyzer.calculate_league_table(df)
    
    return {
        "league_id": league_id,
        "table": table.to_dicts(),
        "total_teams": len(table),
        "generated_at": datetime.now().isoformat()
    }


@app.get("/api/v2/analytics/h2h/{team1}/{team2}")
async def head_to_head(team1: str, team2: str):
    """
    两队历史交锋
    """
    raw_matches = football_client.get_live_matches()
    df = advanced_analyzer.load_matches(raw_matches)
    
    h2h = advanced_analyzer.compare_teams_head_to_head(df, team1, team2)
    
    return {
        "matchup": f"{team1} vs {team2}",
        "analysis": h2h,
        "generated_at": datetime.now().isoformat()
    }


@app.get("/api/v2/analytics/goals-distribution")
async def goals_distribution():
    """
    进球分布分析
    """
    raw_matches = football_client.get_live_matches()
    df = advanced_analyzer.load_matches(raw_matches)
    
    distribution = advanced_analyzer.calculate_goals_distribution(df)
    
    return {
        "analysis": distribution,
        "generated_at": datetime.now().isoformat()
    }


@app.get("/api/v2/ml/features")
async def ml_features():
    """
    ML 特征工程 - 展示 Polars 数据转换能力
    """
    raw_matches = football_client.get_live_matches()
    df = advanced_analyzer.load_matches(raw_matches)
    
    features_df = advanced_analyzer.predict_with_ml_features(df)
    
    return {
        "features": features_df.head(10).to_dicts(),
        "feature_columns": features_df.columns,
        "generated_at": datetime.now().isoformat()
    }


# ============ WebSocket 端点 (高级版) ============

@app.websocket("/ws/v2/live")
async def websocket_live_v2(websocket: WebSocket):
    """
    WebSocket 实时比分推送 - v2 版本
    
    功能：
    - 每30秒推送Live比赛
    - 包含 Polars 高级分析
    - 支持自定义过滤
    """
    await ws_manager.connect(websocket)
    print(f"📱 New WebSocket v2 connection: {websocket.client}")
    
    try:
        # 发送欢迎消息 + 配置
        await websocket.send_json({
            "type": "connected",
            "version": "2.0",
            "message": "Connected to EA FC Live Dashboard v2",
            "features": [
                "live_matches",
                "advanced_stats",
                "league_table",
                "team_form"
            ]
        })
        
        while True:
            # 1. 获取 Live 比赛
            try:
                matches = football_client.get_live_matches()
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                break
            
            if matches:
                # 2. 用 Polars 处理
                df = advanced_analyzer.load_matches(matches)
                
                # 3. 高级分析
                stats = advanced_analyzer.calculate_advanced_stats(df)
                distribution = advanced_analyzer.calculate_goals_distribution(df)
                
                # 4. 推送完整数据
                await websocket.send_json({
                    "type": "live_matches_v2",
                    "match_count": len(matches),
                    "matches": df.head(20).to_dicts(),
                    "stats": stats,
                    "distribution": distribution,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                await websocket.send_json({
                    "type": "no_matches",
                    "message": "No live matches right now",
                    "timestamp": datetime.now().isoformat()
                })
            
            # 等待
            import asyncio
            await asyncio.sleep(30)
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"❌ WebSocket error: {str(e)}")
        ws_manager.disconnect(websocket)


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
