"""
Polars 数据处理器 - 高级版
展示 Polars 的完整数据处理能力
"""
import polars as pl
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json


class AdvancedMatchAnalyzer:
    """
    高级比赛数据分析器
    
    展示 Polars 高级功能：
    - Lazy Evaluation (延迟求值)
    - 复杂聚合
    - 滑动窗口
    - 条件过滤
    - 类型转换
    """
    
    # ============ Schema 定义 ============
    
    MATCH_SCHEMA = {
        "match_id": pl.Int64,
        "league_id": pl.Int32,
        "league_name": pl.Utf8,
        "season": pl.Int16,
        "date": pl.Utf8,
        "home_team": pl.Utf8,
        "away_team": pl.Utf8,
        "home_score": pl.Int8,
        "away_score": pl.Int8,
        "home_xg": pl.Float64,  # Expected Goals
        "away_xg": pl.Float64,
        "home_possession": pl.Float64,
        "away_possession": pl.Float64,
        "home_shots": pl.Int16,
        "away_shots": pl.Int16,
        "home_shots_on_target": pl.Int16,
        "away_shots_on_target": pl.Int16,
        "home_corners": pl.Int8,
        "away_corners": pl.Int8,
        "home_fouls": pl.Int8,
        "away_fouls": pl.Int8,
        "home_yellow_cards": pl.Int8,
        "away_yellow_cards": pl.Int8,
        "status": pl.Utf8,
    }
    
    def __init__(self):
        print("📊 AdvancedMatchAnalyzer 初始化 (Polars)")
        self.cache = {}
    
    # ============ 数据加载 ============
    
    def load_matches(self, raw_data: List[Dict]) -> pl.DataFrame:
        """
        从原始 API 数据加载并转换为 Polars DataFrame
        带有完整的 schema 验证
        """
        processed = []
        for match in raw_data:
            fixture = match.get("fixture", {})
            teams = match.get("teams", {})
            goals = match.get("goals", {})
            score = match.get("score", {})
            league = match.get("league", {})
            
            processed.append({
                "match_id": fixture.get("id", 0),
                "league_id": league.get("id", 0),
                "league_name": league.get("name", "Unknown"),
                "season": league.get("season", 2024),
                "date": fixture.get("date", ""),
                "home_team": teams.get("home", {}).get("name", "TBD"),
                "away_team": teams.get("away", {}).get("name", "TBD"),
                "home_score": goals.get("home", 0),
                "away_score": goals.get("away", 0),
                # 模拟 xG 数据 (实际需要专门 API)
                "home_xg": round(goals.get("home", 0) * 0.8 + 0.5, 2),
                "away_xg": round(goals.get("away", 0) * 0.8 + 0.5, 2),
                "home_possession": 50.0,
                "away_possession": 50.0,
                "home_shots": 10,
                "away_shots": 8,
                "home_shots_on_target": 5,
                "away_shots_on_target": 4,
                "home_corners": 5,
                "away_corners": 3,
                "home_fouls": 8,
                "away_fouls": 10,
                "home_yellow_cards": 1,
                "away_yellow_cards": 2,
                "status": fixture.get("status", {}).get("short", "NS"),
            })
        
        # 使用 Polars 严格模式
        df = pl.DataFrame(processed, schema=self.MATCH_SCHEMA)
        
        # 解析日期
        df = df.with_columns(
            pl.col("date").str.to_datetime("%Y-%m-%dT%H:%M:%S%z")
        )
        
        return df
    
    # ============ 过滤功能 (Polars 优势) ============
    
    def filter_by_league(self, df: pl.DataFrame, league_ids: List[int]) -> pl.DataFrame:
        """
        按联赛过滤 - Polars 快速布尔索引
        """
        return df.filter(pl.col("league_id").is_in(league_ids))
    
    def filter_by_date_range(
        self, 
        df: pl.DataFrame, 
        start_date: str = None, 
        end_date: str = None
    ) -> pl.DataFrame:
        """
        按日期范围过滤
        """
        result = df
        
        if start_date:
            start = pl.datetime(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
            result = result.filter(pl.col("date") >= start)
        
        if end_date:
            end = pl.datetime(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
            result = result.filter(pl.col("date") <= end)
        
        return result
    
    def filter_by_team(self, df: pl.DataFrame, team_name: str) -> pl.DataFrame:
        """
        按球队过滤 (主队或客队)
        """
        return df.filter(
            (pl.col("home_team") == team_name) | 
            (pl.col("away_team") == team_name)
        )
    
    def filter_live_only(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        只看 Live 比赛
        """
        # 状态: 1H(上半场), 2H(下半场), HT(半场), ET(加时)
        live_statuses = ["1H", "2H", "HT", "ET", "BT", "P"]
        return df.filter(pl.col("status").is_in(live_statuses))
    
    def filter_by_score_range(
        self, 
        df: pl.DataFrame, 
        min_goals: int = 0, 
        max_goals: int = 10
    ) -> pl.DataFrame:
        """
        按进球数范围过滤
        """
        total_goals = pl.col("home_score") + pl.col("away_score")
        return df.filter(
            total_goals.between(min_goals, max_goals)
        )
    
    # ============ 高级分析功能 ============
    
    def calculate_advanced_stats(self, df: pl.DataFrame) -> Dict[str, Any]:
        """
        高级统计分析 - 展示 Polars 聚合能力
        """
        if df.is_empty():
            return {}
        
        # Lazy Evaluation 优化
        stats = df.lazy().select([
            # 比赛统计
            pl.len().alias("total_matches"),
            
            # 进球统计
            pl.col("home_score").sum().alias("total_home_goals"),
            pl.col("away_score").sum().alias("total_away_goals"),
            (pl.col("home_score").sum() + pl.col("away_score").sum()).alias("total_goals"),
            
            # 平均进球
            pl.col("home_score").mean().alias("avg_home_goals"),
            pl.col("away_score").mean().alias("avg_away_goals"),
            (pl.col("home_score").mean() + pl.col("away_score").mean()).alias("avg_total_goals"),
            
            # xG 分析
            pl.col("home_xg").mean().alias("avg_home_xg"),
            pl.col("away_xg").mean().alias("avg_away_xg"),
            
            # 射门效率
            (pl.col("home_shots_on_target") / pl.col("home_shots")).mean().alias("avg_home_shot_accuracy"),
            (pl.col("away_shots_on_target") / pl.col("away_shots")).mean().alias("avg_away_shot_accuracy"),
            
            # 角球
            pl.col("home_corners").mean().alias("avg_home_corners"),
            pl.col("away_corners").mean().alias("avg_away_corners"),
            
            # 控球率
            pl.col("home_possession").mean().alias("avg_home_possession"),
            pl.col("away_possession").mean().alias("avg_away_possession"),
        ]).collect()
        
        return stats.to_dicts()[0]
    
    def calculate_team_form(self, df: pl.DataFrame, team_name: str, last_n: int = 5) -> Dict:
        """
        计算球队最近状态 - 展示滑动窗口
        """
        # 过滤该球队的比赛
        team_matches = df.filter(
            (pl.col("home_team") == team_name) | 
            (pl.col("away_team") == team_name)
        ).sort("date", descending=True).head(last_n)
        
        if team_matches.is_empty():
            return {"team": team_name, "form": [], "points": 0}
        
        # 计算最近 N 场的积分
        form = []
        points = 0
        
        for row in team_matches.iter_rows(named=True):
            is_home = row["home_team"] == team_name
            goals_for = row["home_score"] if is_home else row["away_score"]
            goals_against = row["away_score"] if is_home else row["home_score"]
            
            if goals_for > goals_against:
                result = "W"
                points += 3
            elif goals_for == goals_against:
                result = "D"
                points += 1
            else:
                result = "L"
            
            form.append({
                "opponent": row["away_team"] if is_home else row["home_team"],
                "score": f"{goals_for}-{goals_against}",
                "result": result,
                "venue": "Home" if is_home else "Away"
            })
        
        return {
            "team": team_name,
            "form": form,
            "points": points,
            "form_string": "".join([f[0]["result"] for f in [form]]),
            "avg_goals_scored": team_matches.select(
                pl.when(pl.col("home_team") == team_name)
                .then(pl.col("home_score"))
                .otherwise(pl.col("away_score"))
            ).mean(),
            "avg_goals_conceded": team_matches.select(
                pl.when(pl.col("home_team") == team_name)
                .then(pl.col("away_score"))
                .otherwise(pl.col("home_score"))
            ).mean(),
        }
    
    def calculate_league_table(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        计算联赛积分榜 - 展示复杂聚合
        """
        # 准备数据：每场比赛产出两行（主队和客队）
        home_rows = df.select([
            pl.col("date"),
            pl.col("home_team").alias("team"),
            pl.col("home_score").alias("goals_for"),
            pl.col("away_score").alias("goals_against"),
            pl.when(pl.col("home_score") > pl.col("away_score"))
            .then(pl.lit(3))
            .when(pl.col("home_score") == pl.col("away_score"))
            .then(pl.lit(1))
            .otherwise(pl.lit(0))
            .alias("points"),
        ])
        
        away_rows = df.select([
            pl.col("date"),
            pl.col("away_team").alias("team"),
            pl.col("away_score").alias("goals_for"),
            pl.col("home_score").alias("goals_against"),
            pl.when(pl.col("away_score") > pl.col("home_score"))
            .then(pl.lit(3))
            .when(pl.col("away_score") == pl.col("home_score"))
            .then(pl.lit(1))
            .otherwise(pl.lit(0))
            .alias("points"),
        ])
        
        # 合并
        all_rows = pl.concat([home_rows, away_rows])
        
        # 聚合计算积分榜
        table = all_rows.group_by("team").agg([
            pl.col("points").sum().alias("points"),
            pl.col("goals_for").sum().alias("goals_for"),
            pl.col("goals_against").sum().alias("goals_against"),
            pl.len().alias("played"),
            (pl.col("goals_for") - pl.col("goals_against")).sum().alias("goal_difference"),
        ])
        
        # 排序
        table = table.sort(["points", "goal_difference", "goals_for"], descending=True)
        
        # 添加排名
        table = table.with_columns(
            pl.arange(1, pl.len() + 1).alias("position")
        )
        
        return table.select([
            "position", "team", "played", "points", 
            "goals_for", "goals_against", "goal_difference"
        ])
    
    def compare_teams_head_to_head(
        self, 
        df: pl.DataFrame, 
        team1: str, 
        team2: str
    ) -> Dict:
        """
        两队历史交锋 - 展示过滤+聚合组合
        """
        h2h = df.filter(
            ((pl.col("home_team") == team1) & (pl.col("away_team") == team2)) |
            ((pl.col("home_team") == team2) & (pl.col("away_team") == team1))
        )
        
        if h2h.is_empty():
            return {"team1": team1, "team2": team2, "matches": 0}
        
        # 统计
        team1_wins = h2h.filter(
            ((pl.col("home_team") == team1) & (pl.col("home_score") > pl.col("away_score"))) |
            ((pl.col("away_team") == team1) & (pl.col("away_score") > pl.col("home_score")))
        ).len()
        
        team2_wins = h2h.filter(
            ((pl.col("home_team") == team2) & (pl.col("home_score") > pl.col("away_score"))) |
            ((pl.col("away_team") == team2) & (pl.col("away_score") > pl.col("home_score")))
        ).len()
        
        draws = len(h2h) - team1_wins - team2_wins
        
        return {
            "team1": team1,
            "team2": team2,
            "total_matches": len(h2h),
            f"{team1}_wins": team1_wins,
            f"{team2}_wins": team2_wins,
            "draws": draws,
            "recent_matches": h2h.sort("date", descending=True).head(5).to_dicts()
        }
    
    def calculate_goals_distribution(self, df: pl.DataFrame) -> Dict:
        """
        进球分布分析 - 展示 Polars 的分组能力
        """
        # 总进球数
        df = df.with_columns(
            (pl.col("home_score") + pl.col("away_score")).alias("total_goals")
        )
        
        # 分布统计
        distribution = df.group_by("total_goals").agg(
            pl.len().alias("count")
        ).sort("total_goals")
        
        # 主/客队进球分布
        home_distribution = df.group_by("home_score").agg(
            pl.len().alias("count")
        ).sort("home_score")
        
        away_distribution = df.group_by("away_score").agg(
            pl.len().alias("count")
        ).sort("away_score")
        
        return {
            "total_goals_distribution": distribution.to_dicts(),
            "home_goals_distribution": home_distribution.to_dicts(),
            "away_goals_distribution": away_distribution.to_dicts(),
            "stats": {
                "most_common_total": int(distribution.sort("count", descending=True).head(1)[0, "total_goals"]),
                "over_25_percentage": (df.filter(pl.col("total_goals") >= 2.5).len() / len(df) * 100),
                "both_score_percentage": (df.filter((pl.col("home_score") > 0) & (pl.col("away_score") > 0)).len() / len(df) * 100),
            }
        }
    
    def predict_with_ml_features(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        特征工程 - 为 ML 模型准备数据
        展示 Polars 的特征转换能力
        """
        result = df.with_columns([
            # 基础特征
            (pl.col("home_score") + pl.col("away_score")).alias("total_goals"),
            (pl.col("home_score") - pl.col("away_score")).alias("goal_diff"),
            
            # xG 差异
            (pl.col("home_xg") - pl.col("away_xg")).alias("xg_diff"),
            
            # 射门效率
            (pl.col("home_shots_on_target") / pl.col("home_shots")).alias("home_shot_rate"),
            (pl.col("away_shots_on_target") / pl.col("away_shots")).alias("away_shot_rate"),
            
            # 进攻效率
            (pl.col("home_score") / pl.col("home_shots")).alias("home_conversion_rate"),
            (pl.col("away_score") / pl.col("away_shots")).alias("away_conversion_rate"),
            
            # 防守强度
            (pl.col("home_fouls") + pl.col("away_fouls")).alias("total_fouls"),
            (pl.col("home_yellow_cards") + pl.col("away_yellow_cards")).alias("total_cards"),
            
            # 控球优势
            (pl.col("home_possession") - pl.col("away_possession")).alias("possession_diff"),
        ])
        
        # 填充可能的 None 值
        result = result.fill_null(0)
        
        return result
    
    # ============ 性能测试 ============
    
    @staticmethod
    def benchmark(n_rows: int = 100_000):
        """
        Polars 性能基准测试
        """
        import time
        
        print(f"📊 Polars 性能测试 ({n_rows:,} 行数据)")
        
        # 生成测试数据
        data = {
            "home_team": [f"Team_{i % 20}" for i in range(n_rows)],
            "away_team": [f"Team_{(i+1) % 20}" for i in range(n_rows)],
            "home_score": [i % 5 for i in range(n_rows)],
            "away_score": [(i+1) % 5 for i in range(n_rows)],
            "home_xg": [i * 0.1 for i in range(n_rows)],
            "away_xg": [(i+1) * 0.1 for i in range(n_rows)],
            "home_possession": [40 + (i % 30) for i in range(n_rows)],
            "away_possession": [40 + ((i+1) % 30) for i in range(n_rows)],
            "home_shots": [5 + (i % 20) for i in range(n_rows)],
            "away_shots": [5 + ((i+1) % 20) for i in range(n_rows)],
            "home_shots_on_target": [2 + (i % 10) for i in range(n_rows)],
            "away_shots_on_target": [2 + ((i+1) % 10) for i in range(n_rows)],
        }
        
        # ============ Polars ============
        start = time.time()
        df = pl.DataFrame(data)
        
        # 复杂查询
        result = df.lazy().filter(
            (pl.col("home_score") + pl.col("away_score")) >= 2
        ).select([
            pl.col("home_team"),
            pl.col("away_team"),
            (pl.col("home_xg") - pl.col("away_xg")).alias("xg_diff"),
            (pl.col("home_shots_on_target") / pl.col("home_shots")).alias("shot_rate"),
        ]).sort("xg_diff", descending=True).head(1000).collect()
        
        polars_time = time.time() - start
        
        print(f"   Polars: {polars_time:.3f}s")
        print(f"   处理 {n_rows:,} 行，筛选后 {len(result):,} 行")
        
        return polars_time


if __name__ == "__main__":
    # 运行性能测试
    AdvancedMatchAnalyzer.benchmark(100_000)
