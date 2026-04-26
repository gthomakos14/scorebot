import requests
from datetime import date
from notifier import send_score_update

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
                self.game_pk = body['dates'][0]['games'][0]['gamePk']
            except (KeyError, IndexError):
                self.game_pk = None
        self.game_status = 'INACTIVE'
        self.scoring_plays = []


    def refresh_scoring_plays(self):
        new_scoring_plays = self.fetch_scoring_plays()
        if new_scoring_plays != self.scoring_plays:
            # Converting to set makes the lookup faster
            existing_scoring_plays = set(self.scoring_plays)
            result = [i for i in new_scoring_plays if i not in existing_scoring_plays]
            for play in result:
                send_score_update(home_team=play['home_abbreviation'],
                                  home_score=play['home_score'],
                                  away_team=play['away_abbreviation'],
                                  away_score=play['away_score'],
                                  inning=f"{play['inning_half'].capitalize()} {play['inning']}",
                                  description=play['description'])

            self.scoring_plays = new_scoring_plays


    def fetch_scoring_plays(self):
        """Returns all scoring plays from the live feed"""
        url = f"https://statsapi.mlb.com/api/v1.1/game/{self.game_pk}/feed/live"
        data = requests.get(url).json()

        all_plays = data["liveData"]["plays"]["allPlays"]

        return [
            {
                "home_abbreviation": data['gameData']['teams']['home']['abbreviation'],
                "away_abbreviation": data['gameData']['teams']['away']['abbreviation'],
                "description": play["result"]["description"],
                "event": play["result"]["event"],
                "away_score": play["result"]["awayScore"],
                "home_score": play["result"]["homeScore"],
                "inning": play["about"]["inning"],
                "inning_half": play["about"]["halfInning"],
                "play_index": play["about"]["atBatIndex"],
            }
            for play in all_plays
            if play["about"]["isScoringPlay"]
        ]
    

   
