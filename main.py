import time
from game_tracker import Tracker
import datetime as dt


def main():
    tracker = Tracker()
    while True:
        tracker.refresh_scoring_plays()
        print(f'{dt.datetime.now()} ~~~ Checking again in 1 minute')
        time.sleep(60)

    # send_score_update(home_team='TB',
    #                   home_score=0,
    #                   away_team='NYY',
    #                   away_score=1,
    #                   description='Cody Bellinger out on a sacrifice fly to right fielder Jonny DeLuca. Aaron Judge scores.',
    #                   inning='Top 7')

if __name__ == '__main__':
    main()