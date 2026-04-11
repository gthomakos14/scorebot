from notifier import send_score_update


def main():
    send_score_update(home_team='TB',
                      home_score=0,
                      away_team='NYY',
                      away_score=1,
                      description='Cody Bellinger out on a sacrifice fly to right fielder Jonny DeLuca. Aaron Judge scores.',
                      inning='Top 7')

if __name__ == '__main__':
    main()