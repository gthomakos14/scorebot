import time
from game_tracker import Tracker
import datetime as dt
from notifier import send_error


def main():
    tracker = Tracker()
    # TODO: Have smarter functionality for making this go dormant
    counter = 0
    while (tracker.game_status != 'FINAL') or (counter < 300):
        try:
            tracker.refresh()
            # TODO: Better way to do this is to fetch game start time. But have to check how the API does rain delays
            if tracker.game_status == 'PREVIEW':
                print(f'{dt.datetime.now()} ~~~ Game not started. Checking again in 15 minutes')
                time.sleep(900)
                counter += 15
            else:
                if counter % 5 == 0:
                    print(f'{dt.datetime.now()} ~~~ Game is live. Next message in 5 minutes')
                counter += 1
                time.sleep(60)
        except Exception as e:
            send_error(e)


if __name__ == '__main__':
    main()