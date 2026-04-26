import requests
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_score_update(home_team: str,
                      home_score: int, 
                      away_team: str, 
                      away_score: int,
                      inning: str,
                      description: str) -> bool:
    msg = f"""{away_team} {away_score} — {home_score} {home_team}
{inning}
{'~'*8}
{description}
{'~'*8}"""
    payload = {
        "content": msg
    }

    response = requests.post(DISCORD_URL, json=payload)
    return response.status_code == 204


def send_error(error):
    response = requests.post(DISCORD_URL, json={"content": str(error)})
    return response.status_code == 204
