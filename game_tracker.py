import requests
from datetime import date

BASE_URL = "https://statsapi.mlb.com/api/v1"
# TODO: Future functionality can have the team ID in the config if other teams become important
YANKEES_ID = 147

class Tracker:
    def __init__(self, game_pk=None):
        if game_pk is not None:
            self.game_pk = game_pk
        else:
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
        self.game_status = 'INACTIVE'
        self.scoring_plays = []


    def get_game_pk(self):
        return self.game_pk
    

    def get_scoring_plays(self):
        return self.scoring_plays
    

    def set_scoring_plays(self, new_scoring_plays):
        self.scoring_plays = new_scoring_plays
