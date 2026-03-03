"""
Mock Sports Data - Realistic sample data when API is unavailable
"""
from datetime import datetime, timedelta
import random

def get_mock_sports_data():
    """Generate realistic mock data for demo"""
    
    now = datetime.now()
    
    # Basketball games
    basketball_matches = [
        {
            "id": 1,
            "date": (now + timedelta(hours=2)).isoformat(),
            "status": {"short": "NS", "long": "Not Started"},
            "league": {"id": 12, "name": "NBA", "logo": "https://cdn.nba.com//uploads/nba-logos/12.svg"},
            "teams": {
                "home": {"id": 132, "name": "Atlanta Hawks", "logo": "https://cdn.nba.com/teams/logos/nba/132.svg"},
                "away": {"id": 156, "name": "Portland Trail Blazers", "logo": "https://cdn.nba.com/teams/logos/nba/156.svg"}
            },
            "scores": {"home": {"total": None}, "away": {"total": None}},
            "sport": "basketball",
            "venue": "State Farm Arena"
        },
        {
            "id": 2,
            "date": now.isoformat(),
            "status": {"short": "Q2", "long": "Quarter 2"},
            "league": {"id": 12, "name": "NBA", "logo": "https://cdn.nba.com/logos/nba/12.svg"},
            "teams": {
                "home": {"id": 161, "name": "Los Angeles Lakers", "logo": "https://cdn.nba.com/teams/logos/nba/161.svg"},
                "away": {"id": 140, "name": "Boston Celtics", "logo": "https://cdn.nba.com/teams/logos/nba/140.svg"}
            },
            "scores": {"home": {"total": 58}, "away": {"total": 52}},
            "sport": "basketball",
            "venue": "Crypto.com Arena"
        },
        {
            "id": 3,
            "date": (now - timedelta(hours=3)).isoformat(),
            "status": {"short": "FT", "long": "Final"},
            "league": {"id": 116, "name": "NCAA", "logo": "https://cdn.ncaa.com/imagesNCAA-logo.svg"},
            "teams": {
                "home": {"id": 200, "name": "Duke Blue Devils", "logo": "https://a.espncdn.com-i.cdn.turner.com/cron7a4ff00d-9078-43fd-8228-bfa3389884d4/ncaa/team500/150.svg"},
                "away": {"id": 204, "name": "UNC Tar Heels", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/153.svg"}
            },
            "scores": {"home": {"total": 87}, "away": {"total": 79}},
            "sport": "basketball",
            "venue": "Cameron Indoor Stadium"
        },
        {
            "id": 4,
            "date": (now + timedelta(hours=5)).isoformat(),
            "status": {"short": "NS", "long": "Not Started"},
            "league": {"id": 12, "name": "NBA", "logo": "https://cdn.nba.com/logos/nba/12.svg"},
            "teams": {
                "home": {"id": 151, "name": "New York Knicks", "logo": "https://cdn.nba.com/teams/logos/nba/151.svg"},
                "away": {"id": 158, "name": "San Antonio Spurs", "logo": "https://cdn.nba.com/teams/logos/nba/158.svg"}
            },
            "scores": {"home": {"total": None}, "away": {"total": None}},
            "sport": "basketball",
            "venue": "Madison Square Garden"
        },
    ]
    
    # Football (Soccer) matches
    football_matches = [
        {
            "id": 101,
            "date": now.isoformat(),
            "status": {"short": "2H", "long": "Second Half"},
            "league": {"id": 39, "name": "Premier League", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/7y3f0ZPi9I0d4X4c5t6b9a_LOGO.svg"},
            "teams": {
                "home": {"id": 50, "name": "Manchester United", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/50.png"},
                "away": {"id": 49, "name": "Liverpool", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/49.png"}
            },
            "scores": {"home": {"total": 2}, "away": {"total": 1}},
            "sport": "football",
            "venue": "Old Trafford"
        },
        {
            "id": 102,
            "date": (now + timedelta(hours=1)).isoformat(),
            "status": {"short": "NS", "long": "Not Started"},
            "league": {"id": 140, "name": "La Liga", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/LaLiga_Logo.svg"},
            "teams": {
                "home": {"id": 529, "name": "Barcelona", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/barcelona.svg"},
                "away": {"id": 541, "name": "Real Madrid", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/real-madrid.svg"}
            },
            "scores": {"home": {"total": None}, "away": {"total": None}},
            "sport": "football",
            "venue": "Camp Nou"
        },
        {
            "id": 103,
            "date": (now - timedelta(hours=2)).isoformat(),
            "status": {"short": "FT", "long": "Full Time"},
            "league": {"id": 78, "name": "Bundesliga", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/Bundesliga_Logo.svg"},
            "teams": {
                "home": {"id": 157, "name": "Bayern Munich", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/bayern.svg"},
                "away": {"id": 163, "name": "Borussia Dortmund", "logo": "https://ssl.gstatic.com/onebox/media/sports/logos/dortmund.svg"}
            },
            "scores": {"home": {"total": 4}, "away": {"total": 2}},
            "sport": "football",
            "venue": "Allianz Arena"
        },
    ]
    
    return {
        "basketball": basketball_matches,
        "football": football_matches
    }

def get_mock_all_sports():
    """Get all sports with mock data"""
    data = get_mock_sports_data()
    
    result = {}
    
    for sport_key, matches in data.items():
        result[sport_key] = {
            "name": sport_key.title(),
            "emoji": "🏀" if sport_key == "basketball" else "⚽",
            "count": len(matches),
            "matches": matches
        }
    
    # Add empty entries for other sports to show tabs
    other_sports = ["nba", "nfl", "hockey", "baseball", "afl", "formula1", "handball", "mma", "rugby", "volleyball"]
    for sport in other_sports:
        result[sport] = {
            "name": sport.title(),
            "emoji": "🏈" if sport == "nfl" else "🏒" if sport == "hockey" else "🏀",
            "count": 0,
            "matches": []
        }
    
    return result
