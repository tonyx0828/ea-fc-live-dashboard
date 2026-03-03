"""
ESPN Sports API Client - Free real-time sports data
"""
import requests
from datetime import datetime

# ESPN API endpoints
ESPN_APIS = {
    "nba": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
    "nfl": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "nhl": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
    "mlb": "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard",
    "ncaab": "https://site.api.espn.com/apis/site/v2/sports/basketball/college-sports/scoreboard?dates=20250201-20251231",
    "ncaaf": "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20250201-20251231",
}

def get_espn_data(sport="nba"):
    """Fetch data from ESPN API"""
    url = ESPN_APIS.get(sport)
    if not url:
        return []
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"ESPN API error: {e}")
    return {}

def convert_espn_to_our_format(espn_data, sport_key):
    """Convert ESPN format to our format"""
    matches = []
    
    events = espn_data.get("events", [])
    
    for event in events:
        competition = event.get("competitions", [{}])[0]
        
        # Get teams
        competitors = competition.get("competitors", [])
        home_team = competitors[0] if len(competitors) > 0 else {}
        away_team = competitors[1] if len(competitors) > 1 else {}
        
        # Get scores
        home_score = home_team.get("score", "0")
        away_score = away_team.get("score", "0")
        
        # Get status
        status = competition.get("status", {})
        status_desc = status.get("description", "")
        period = status.get("period", 0)
        
        # Convert status
        if "Final" in status_desc:
            status_short = "FT"
        elif period > 0:
            status_short = f"Q{period}"
        else:
            status_short = "NS"
        
        # Get date
        date_str = event.get("date", "")
        
        # Get league
        league = sport_key.upper()
        
        match = {
            "id": event.get("id", ""),
            "date": date_str,
            "status": {"short": status_short, "long": status_desc},
            "league": {"name": league, "id": sport_key},
            "teams": {
                "home": {
                    "id": home_team.get("id", ""),
                    "name": home_team.get("team", {}).get("displayName", "TBD"),
                    "logo": home_team.get("team", {}).get("logo", "")
                },
                "away": {
                    "id": away_team.get("id", ""),
                    "name": away_team.get("team", {}).get("displayName", "TBD"),
                    "logo": away_team.get("team", {}).get("logo", "")
                }
            },
            "scores": {
                "home": {"total": int(home_score) if home_score.isdigit() else None},
                "away": {"total": int(away_score) if away_score.isdigit() else None}
            },
            "sport": sport_key
        }
        
        matches.append(match)
    
    return matches

def get_all_espn_sports():
    """Get all sports data from ESPN"""
    result = {}
    
    sport_info = {
        "nba": {"name": "NBA", "emoji": "🏀"},
        "nfl": {"name": "NFL", "emoji": "🏈"},
        "nhl": {"name": "NHL", "emoji": "🏒"},
        "mlb": {"name": "MLB", "emoji": "⚾"},
    }
    
    for sport_key in ["nba", "nhl"]:
        print(f"Fetching {sport_key} from ESPN...")
        espn_data = get_espn_data(sport_key)
        matches = convert_espn_to_our_format(espn_data, sport_key)
        
        result[sport_key] = {
            "name": sport_info.get(sport_key, {}).get("name", sport_key.title()),
            "emoji": sport_info.get(sport_key, {}).get("emoji", "🏆"),
            "count": len(matches),
            "matches": matches
        }
        print(f"  Got {len(matches)} {sport_key} games")
    
    # Add placeholder for other sports
    other_sports = ["basketball", "football", "nba", "nfl", "hockey", "baseball", "afl", "formula1", "handball", "mma", "rugby", "volleyball"]
    for sport in other_sports:
        if sport not in result:
            result[sport] = {
                "name": sport.title(),
                "emoji": "🏆",
                "count": 0,
                "matches": []
            }
    
    return result

if __name__ == "__main__":
    # Test
    data = get_all_espn_sports()
    print(f"\nTotal sports: {len(data)}")
    for k, v in data.items():
        if v["count"] > 0:
            print(f"  {k}: {v['count']} matches")
