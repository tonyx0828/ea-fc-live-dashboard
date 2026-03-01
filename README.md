# Live Sports Dashboard

Real-time sports data dashboard with WebSocket streaming

## 🎯 Project Overview

A multi-sport live dashboard that displays real-time match data from various sports leagues:
- ⚽ Football (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)
- 🏀 NBA (Basketball)
- 🏈 NFL (American Football)
- 🏒 NHL (Ice Hockey)

## 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| **FastAPI** | REST API + WebSocket server |
| **WebSocket** | Real-time data streaming |
| **Polars** | High-performance data processing |
| **Docker** | Container deployment |
| **Render** | Cloud hosting |

## 🚀 Features

- Real-time match updates
- Multiple sports support
- REST API with filters
- Polars data analytics
- Docker containerization
- Cloud deployment ready

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/sports/live` | All live matches |
| `GET /api/sports/football/live` | Football only |
| `GET /api/sports/nba/live` | NBA only |
| `GET /api/sports/nfl/live` | NFL only |
| `GET /api/sports/hockey/live` | NHL only |
| `GET /docs` | API documentation |

## 🏃 Quick Start

### Local

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env
uvicorn main:app --reload
```

### Docker

```bash
docker build -t live-sports .
docker run -p 8000:8000 live-sports
```

## 🌐 Live Demo

**Frontend**: https://ea-fc-live-dashboard.onrender.com

**API Docs**: https://ea-fc-live-dashboard.onrender.com/docs

## 📁 Project Structure

```
├── main.py                 # FastAPI app
├── config.py              # Configuration
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker config
├── api/
│   ├── football_client.py # Football API client
│   ├── sports_client.py  # Multi-sport client
│   └── routes.py          # API routes
├── processing/
│   ├── polars_processor.py
│   └── advanced_analyzer.py
└── static/
    └── index.html         # Frontend
```

## 📝 License

MIT
