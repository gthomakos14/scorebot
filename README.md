# Baseball Game Tracker

A lightweight Python tool that monitors a live MLB game in real time and pushes score update notifications as plays happen.

## Overview

Baseball Game Tracker polls the MLB Stats API for live game data and fires notifications whenever a scoring play occurs. It's built around a single `Tracker` object that manages game state and handles the polling loop.

## Features

- Automatically finds today's game for a configured team
- Detects scoring plays in real time and sends notifications
- Tracks game status (`Preview`, `Live`, `Final`) and exits cleanly when the game ends
- Single API call per refresh cycle — no redundant requests

## Requirements

- Python 3.8+
- `requests`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set the following constants before running:

```python
BASE_URL = "https://statsapi.mlb.com/api/v1"
TEAM_ID  = 147  # Replace with your team's MLB team ID
```

You can find your team's ID via the MLB Stats API:
```
https://statsapi.mlb.com/api/v1/teams?sportId=1
```

## Usage

```bash
python main.py
```

On startup, the tracker fetches the game PK for today's game and begins polling. Score updates are pushed via `send_score_update()` — wire this to whatever notification backend you prefer (Slack, SMS, etc.).


## Limitations

- Does not currently support doubleheaders — only the first game of the day is tracked
- Notification delivery depends on your implementation of `send_score_update()`
- Only one team at a time is tracked and it's difficult to configure
- Error messaging sends to the same channel as the score updates
- Not very portable

## License

MIT