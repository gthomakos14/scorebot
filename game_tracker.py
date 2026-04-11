import requests
from datetime import date

BASE_URL = "https://statsapi.mlb.com/api/v1"
# TODO: Future functionality can have the team ID in the config if other teams become important
YANKEES_ID = 147

def get_game_pk(today=''):
    # Conditional allows other dates to be passed
    if len(today) == 0:
        today = date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/schedule?sportId=1&teamId={YANKEES_ID}&date={today}"
    result = requests.get(url)
    assert result.status_code == 200, f'Status code on game Pk fetch was {result.status_code}'

    body = result.json()
    try:
        # TODO: This does not support double headers
        game_pk = body['dates'][0]['games'][0]['gamePk']
        return game_pk
    except (KeyError, IndexError):
        return None