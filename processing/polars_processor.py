"""
Polars 数据处理器
展示如何用 Polars 处理足球数据

为什么选 Polars 而非 Pandas？
- 速度快 5-10x
- 内存效率更高
- 延迟求值 (Lazy Evaluation)
- 更类型安全
"""
import polars as pl
from typing import List, Dict, Any, Optional
from datetime import datetime


class MatchAnalyzer:
    """
    比赛数据分析器
    使用 Polars 进行高效数据处理
    """
    
    # 定义数据结构 schema
    MATCH_SCHEMA = {
        "match_id": pl.Int64,
        "home_team": pl.Utf8,
        "away_team": pl.Utf8,
        "home_score": pl.Int8,
        "away_score": pl.Int8,
        "match_time": pl.Utf8,
        "home_possession": pl.Float64,
        "away_possession": pl.Float64,
        "home_shots": pl.Int16,
        "away_shots": pl.Int16,
        "home_shots_on_target": pl.Int16,
        "away_shots_on_target": pl.Int16,
    }
    
    def __init__(self):
        print("📊 MatchAnalyzer 初始化 (使用 Polars)")
    
    # ============ 核心方法 ============
    
    def process_live_matches(self, matches: List[Dict]) -> List[Dict]:
        """
        处理 Live 比赛数据
        将 API 返回的原始数据转换为 Polars DataFrame 处理
        """
        if not matches:
            return []
        
        # 1. 转换为 Polars 兼容格式
        processed = []
        for match in matches:
            fixture = match.get("fixture", {})
            teams = match.get("teams", {})
            goals = match.get("goals", {})
            score = match.get("score", {})
            
            processed.append({
                "match_id": fixture.get("id"),
                "home_team": teams.get("home", {}).get("name"),
                "away_team": teams.get("away", {}).get("name"),
                "home_score": goals.get("home", 0),
                "away_score": goals.get("away", 0),
                "status": fixture.get("status", {}).get("short"),
                "match_time": fixture.get("date"),
                # 模拟数据
                "home_possession": 50.0,
                "away_possession": 50.0,
                "home_shots": 10,
                "away_shots": 8,
            })
        
        # 2. 用 Polars 处理
        df = pl.DataFrame(processed)
        
        # Polars 快速计算
        result = df.select([
            pl.col("match_id"),
            pl.col("home_team"),
            pl.col("away_team"),
            pl.col("home_score"),
            pl.col("away_score"),
            pl.col("status"),
            # 计算进球概率
            (pl.col("home_score") + pl.col("away_score")).alias("total_goals"),
        ])
        
        return result.to_dicts()
    
    def analyze_match_stats(self, stats: List[Dict]) -> Dict[str, Any]:
        """
        分析比赛统计数据
        展示 Polars 的聚合计算能力
        """
        if not stats:
            return {}
        
        # 提取统计数据
        team_stats = []
        for stat in stats:
            team_name = stat.get("team", {}).get("name", "Unknown")
            metrics = stat.get("statistics", {})
            
            team_stats.append({
                "team": team_name,
                "shots": metrics.get("shots", 0),
                "shots_on_goal": metrics.get("shotsOnGoal", 0),
                "possession": int(metrics.get("possession", "0").replace("%", "")),
                "passes": metrics.get("passes", 0),
                "pass_accuracy": int(metrics.get("passAccuracy", "0").replace("%", "")),
                "fouls": metrics.get("fouls", 0),
                "corners": metrics.get("corners", 0),
            })
        
        if not team_stats:
            return {}
        
        # 用 Polars 分析
        df = pl.DataFrame(team_stats)
        
        # 计算转化率 (射门进球率)
        df = df.with_columns(
            (pl.col("shots_on_goal") / pl.col("shots")).alias("shot_accuracy")
        )
        
        # 整体统计
        analysis = df.select([
            pl.col("shots").sum().alias("total_shots"),
            pl.col("shots_on_goal").sum().alias("total_shots_on_target"),
            pl.col("possession").mean().alias("avg_possession"),
            pl.col("passes").sum().alias("total_passes"),
            pl.col("corners").sum().alias("total_corners"),
        ])
        
        return {
            "summary": analysis.to_dicts()[0],
            "teams": df.to_dicts(),
            "generated_at": datetime.now().isoformat()
        }
    
    def predict_outcome(self, stats: List[Dict]) -> Dict[str, Any]:
        """
        预测比赛结果
        展示 Polars 的简单 ML 预处理能力
        
        注意：这是简化版，真实场景需要 ML 模型
        """
        if not stats:
            return {"home_win": 0.33, "draw": 0.33, "away_win": 0.34}
        
        # 用 Polars 构建特征
        features = []
        for stat in stats:
            metrics = stat.get("statistics", {})
            
            shots = metrics.get("shots", 1)
            shots_on = metrics.get("shotsOnGoal", 1)
            possession = int(metrics.get("possession", "50").replace("%", ""))
            
            features.append({
                "shots": shots,
                "shots_on_target": shots_on,
                "possession": possession,
                "attack_strength": shots * 0.3 + shots_on * 0.5 + possession * 0.2
            })
        
        # Polars 计算
        df = pl.DataFrame(features)
        
        # 简单加权
        home_strength = df.filter(pl.lit(True) == pl.lit(True))  # 简化
        
        # 返回预测结果
        total_shots = df.select(pl.col("shots").sum())[0, 0]
        
        return {
            "home_win_prob": 0.40,
            "draw_prob": 0.25,
            "away_win_prob": 0.35,
            "method": "polars_weighted_average",
            "factors": {
                "total_shots": total_shots,
                "avg_possession": df.select(pl.col("possession").mean())[0, 0]
            }
        }
    
    def compare_teams(self, teams_data: List[Dict]) -> Dict[str, Any]:
        """
        对比两队数据
        展示 Polars 的 DataFrame 对比能力
        """
        if len(teams_data) < 2:
            return {}
        
        # 转换为 DataFrame
        df = pl.DataFrame(teams_data)
        
        # 聚合统计
        comparison = df.group_by("team").agg([
            pl.col("goals_for").sum().alias("total_goals"),
            pl.col("goals_against").sum().alias("total_conceded"),
            pl.len().alias("matches_played"),
        ])
        
        # 计算净胜球
        comparison = comparison.with_columns(
            (pl.col("total_goals") - pl.col("total_conceded")).alias("goal_diff")
        )
        
        return comparison.to_dicts()
    
    def calculate_league_table(self, matches: List[Dict]) -> List[Dict]:
        """
        计算联赛积分榜
        展示 Polars 的复杂聚合能力
        """
        if not matches:
            return []
        
        # 准备数据
        rows = []
        for match in matches:
            home = match.get("home_team")
            away = match.get("away_team")
            home_goals = match.get("home_score", 0)
            away_goals = match.get("away_score", 0)
            
            rows.append({"team": home, "goals_for": home_goals, "goals_against": away_goals, "points": 3 if home_goals > away_goals else 1 if home_goals == away_goals else 0})
            rows.append({"team": away, "goals_for": away_goals, "goals_against": home_goals, "points": 3 if away_goals > home_goals else 1 if away_goals == home_goals else 0})
        
        # Polars 聚合
        df = pl.DataFrame(rows)
        
        table = df.group_by("team").agg([
            pl.col("goals_for").sum().alias("GF"),
            pl.col("goals_against").sum().alias("GA"),
            pl.col("points").sum().alias("Points"),
            pl.len().alias("P"),
        ])
        
        # 计算净胜球并排序
        table = table.with_columns(
            (pl.col("GF") - pl.col("GA")).alias("GD")
        ).sort(
            ["Points", "GD", "GF"],
            descending=True
        )
        
        return table.to_dicts()


# ============ 性能对比示例 ============

def benchmark_polars_vs_pandas():
    """
    Polars vs Pandas 性能对比
    
    结果：Polars 通常快 5-10x
    """
    import time
    import pandas as pd
    
    # 生成测试数据：100万行
    n = 1_000_000
    data = {
        "team": ["Team A"] * n,
        "goals": list(range(n)),
        "assists": list(range(n, 2*n)),
        "minutes": [90] * n
    }
    
    # ============ Pandas ============
    start = time.time()
    df_pd = pd.DataFrame(data)
    
    result_pd = df_pd[df_pd["goals"] > 500000].agg({
        "goals": "mean",
        "assists": "mean",
        "minutes": "sum"
    })
    
    pandas_time = time.time() - start
    
    # ============ Polars ============
    start = time.time()
    df_pl = pl.DataFrame(data)
    
    result_pl = df_pl.filter(
        pl.col("goals") > 500000
    ).select([
        pl.col("goals").mean(),
        pl.col("assists").mean(),
        pl.col("minutes").sum()
    ])
    
    polars_time = time.time() - start
    
    print(f"📊 性能对比 (100万行数据):")
    print(f"   Pandas:  {pandas_time:.3f}s")
    print(f"   Polars: {polars_time:.3f}s")
    print(f"   速度提升: {pandas_time/polars_time:.1f}x")


if __name__ == "__main__":
    benchmark_polars_vs_pandas()
