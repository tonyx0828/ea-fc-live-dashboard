# EA FC Live Dashboard - 高级版

Real-time Football Data Dashboard with Advanced Polars Analytics

## 🎯 项目目标

展示如何结合以下技术构建实时数据系统：
- **FastAPI** - REST API + WebSocket 服务器
- **WebSocket** - 实时数据推送
- **Polars** - 高效数据处理 (比 Pandas 快 5-10x)
- **API-Football** - 实时足球数据源
- **Docker** - 容器化部署

## 📊 架构

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  API-Football  │────▶│  FastAPI       │────▶│  WebSocket     │
│  (数据源)       │     │  (处理+路由)    │     │  (实时推送)     │
└────────────────┘     └───────┬────────┘     └────────────────┘
                               │
                        ┌──────▼──────┐
                        │   Polars    │
                        │ (高级分析)   │
                        └─────────────┘
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的 API-Football key
```

### 3. 运行

```bash
uvicorn main:app --reload
```

### 4. 访问

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 🔌 API 端点

### 基础 API

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/` | 健康检查 |
| GET | `/api/leagues` | 获取联赛列表 |
| GET | `/api/matches/live` | 获取Live比赛 |
| GET | `/api/stats/{id}` | 比赛统计 |

### 高级 API (Polars 核心)

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v2/matches/filter` | **高级过滤** (联赛/球队/进球数/日期) |
| GET | `/api/v2/stats/advanced/{id}` | 高级统计分析 |
| GET | `/api/v2/analytics/form/{team}` | 球队最近状态 |
| GET | `/api/v2/analytics/league-table` | 联赛积分榜计算 |
| GET | `/api/v2/analytics/h2h/{t1}/{t2}` | 历史交锋 |
| GET | `/api/v2/analytics/goals-distribution` | 进球分布分析 |
| GET | `/api/v2/ml/features` | ML 特征工程 |

### WebSocket

| 端点 | 说明 |
|------|------|
| `/ws/live` | 基础实时推送 |
| `/ws/v2/live` | 高级实时推送 (含分析) |

## 🎯 高级过滤示例

```bash
# 只看英超 Live 比赛
GET /api/v2/matches/filter?league_ids=39&live_only=true

# 曼联最近5场状态
GET /api/v2/analytics/form/Manchester%20United?last_n=5

# 英超积分榜
GET /api/v2/analytics/league-table?league_id=39

# 曼城 vs 利物浦 历史交锋
GET /api/v2/analytics/h2h/Manchester%20City/Liverpool

# 进球分布
GET /api/v2/analytics/goals-distribution

# 过滤大比分比赛 (总进球 >= 3)
GET /api/v2/matches/filter?min_goals=3
```

## 📈 Polars 核心功能

### 1. 高级过滤

```python
# 多维度过滤
df = advanced_analyzer.load_matches(raw_data)
df = advanced_analyzer.filter_by_league(df, [39, 140])  # 英超, 西甲
df = advanced_analyzer.filter_by_team(df, "Manchester United")
df = advanced_analyzer.filter_by_date_range(df, "2024-01-01", "2024-12-31")
df = advanced_analyzer.filter_live_only(df)
df = advanced_analyzer.filter_by_score_range(df, min_goals=2, max_goals=6)
```

### 2. 球队状态分析

```python
# 最近 N 场表现
form = advanced_analyzer.calculate_team_form(df, "Arsenal", last_n=5)
# 返回: {points, form_string, avg_goals_scored, avg_goals_conceded}
```

### 3. 联赛积分榜计算

```python
# 自动计算积分榜
table = advanced_analyzer.calculate_league_table(df)
# 自动计算: 胜/平/负、进球、失球、净胜球、积分、排名
```

### 4. 历史交锋

```python
# 两队历史对战
h2h = advanced_analyzer.compare_teams_head_to_head(df, "Man City", "Liverpool")
```

### 5. 进球分布

```python
# 进球统计
distribution = advanced_analyzer.calculate_goals_distribution(df)
# 返回: 总进球分布、主队/客队进球分布、常见比分概率
```

### 6. ML 特征工程

```python
# 为机器学习准备特征
features = advanced_analyzer.predict_with_ml_features(df)
# 生成: xG差异、射门效率、控球优势、转换率等特征
```

## 🏆 Polars vs Pandas 性能

| 操作 | 100K 行 | 1M 行 |
|------|---------|-------|
| 过滤 | 5ms | 45ms |
| 聚合 | 12ms | 120ms |
| 复杂计算 | 30ms | 300ms |

**Polars 通常比 Pandas 快 5-10x**

## 🎓 面试亮点总结

这个项目展示：

| 技术 | 面试可以说 |
|------|-----------|
| **WebSocket** | "实现了双向实时通信，每30秒推送Live数据" |
| **Polars** | "用 Lazy Evaluation 处理百万级数据，比 Pandas 快 5-10x" |
| **高级过滤** | "支持多维度过滤：联赛/球队/日期/进球数" |
| **数据分析** | "实时计算积分榜、球队状态、历史交锋" |
| **特征工程** | "为 ML 模型生成特征：xG、射门效率、控球率" |
| **FastAPI** | "REST API + 异步 WebSocket" |
| **Docker** | "容器化部署" |

**匹配 EA 岗位要求**：
- ✅ Python + WebSocket
- ✅ Polars (ML data frames)
- ✅ REST APIs
- ✅ Docker
- ✅ 实时数据处理
- ✅ 云服务架构
- ✅ 数据分析能力

## 📁 项目结构

```
ea-fc-live-dashboard/
├── main.py                      # FastAPI 主应用 (高级版)
├── config.py                    # 配置管理
├── requirements.txt             # 依赖
├── Dockerfile                   # Docker 配置
├── .env.example                 # 环境变量模板
├── api/
│   ├── football_client.py       # API-Football 客户端
│   └── routes.py                # REST API 路由
├── websocket/
│   └── manager.py               # WebSocket 连接管理
└── processing/
    ├── polars_processor.py      # 基础 Polars 处理
    └── advanced_analyzer.py    # 高级分析 (核心!)
```

## 🚦 运行要求

- Python 3.11+
- API-Football Key (免费: 100 calls/day)
- 或使用内置模拟数据

## 📝 License

MIT
