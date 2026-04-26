import requests
from datetime import date
from notifier import send_score_update

BASE_URL = "https://statsapi.mlb.com/api/v1"
# TODO: Future functionality can have the team ID in the config if other teams become important
TEAM_ID = 147

# {'Athletics': 133,
#  'Pittsburgh Pirates': 134,
#  'San Diego Padres': 135,
#  'Seattle Mariners': 136,
#  'San Francisco Giants': 137,
#  'St. Louis Cardinals': 138,
#  'Tampa Bay Rays': 139,
#  'Texas Rangers': 140,
#  'Toronto Blue Jays': 141,
#  'Minnesota Twins': 142,
#  'Philadelphia Phillies': 143,
#  'Atlanta Braves': 144,
#  'Chicago White Sox': 145,
#  'Miami Marlins': 146,
#  'New York Yankees': 147,
#  'Milwaukee Brewers': 158,
#  'Los Angeles Angels': 108,
#  'Arizona Diamondbacks': 109,
#  'Baltimore Orioles': 110,
#  'Boston Red Sox': 111,
#  'Chicago Cubs': 112,
#  'Cincinnati Reds': 113,
#  'Cleveland Guardians': 114,
#  'Colorado Rockies': 115,
#  'Detroit Tigers': 116,
#  'Houston Astros': 117,
#  'Kansas City Royals': 118,
#  'Los Angeles Dodgers': 119,
#  'Washington Nationals': 120,
#  'New York Mets': 121}

class Tracker:
    def __init__(self):
        self.game_pk = self.fetch_game_pk()
        print(f'Current game PK is {self.game_pk}')
        # TODO: Build out the functionality around game status
        self.game_status = 'INACTIVE'
        self.scoring_plays = self.fetch_scoring_plays()


    def refresh_scoring_plays(self):
        new_scoring_plays = self.fetch_scoring_plays()
        if new_scoring_plays != self.scoring_plays:
            result = [i for i in new_scoring_plays if i not in self.scoring_plays]
            for play in result:
                send_score_update(home_team=play['home_abbreviation'],
                                  home_score=play['home_score'],
                                  away_team=play['away_abbreviation'],
                                  away_score=play['away_score'],
                                  inning=f"{play['inning_half'].capitalize()} {play['inning']}",
                                  description=play['description'])

            self.scoring_plays = new_scoring_plays


    def fetch_game_pk(self):
        today = date.today().strftime("%Y-%m-%d")
        url = f"{BASE_URL}/schedule?sportId=1&teamId={TEAM_ID}&date={today}"
        result = requests.get(url)
        assert result.status_code == 200, f'Status code on game Pk fetch was {result.status_code}'

        body = result.json()
        try:
            # TODO: This does not support double headers
            return body['dates'][0]['games'][0]['gamePk']
        except (KeyError, IndexError):
            return None


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
            if play["about"].get('isScoringPlay', False)
        ]
    

   
