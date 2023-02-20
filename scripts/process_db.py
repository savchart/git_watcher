import requests
import time
import os
import argparse
from datetime import datetime
from sqlalchemy import create_engine, text, insert, Table, MetaData

EVENT_TYPES = ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']


def init_db():
    engine = create_engine('sqlite:///app.db')
    with engine.connect() as connection:
        connection.execute(text('DROP TABLE IF EXISTS event'))
        connection.execute(text('CREATE TABLE event (id INTEGER PRIMARY KEY, '
                                'event_type TEXT, '
                                'repository TEXT, '
                                'created_at TIMESTAMP)'))
        connection.commit()


def stream_events(interval, limit):
    url = "https://api.github.com/events"
    headers = {
        "Accept": "application/vnd.github+json"
    }
    params = {
        "per_page": 100
    }

    engine = create_engine('sqlite:///app.db')
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"An error occurred while streaming events from the GitHub API: {e}")
            time.sleep(interval / 2)
            continue

        events = response.json()
        for event in events:
            if (event_type := event.get("type")) in ("WatchEvent", "PullRequestEvent", "IssuesEvent"):
                repository = event.get("repo", {}).get("name")
                timestamp_str = event.get("created_at")
                if repository and timestamp_str:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                    with engine.connect() as conn:
                        event_table = Table('event', MetaData(), autoload_with=engine)
                        event_row = insert(event_table).values(event_type=event_type,
                                                               repository=repository,
                                                               created_at=timestamp)
                        conn.execute(event_row)
                        conn.commit()
        limit -= 1
        if limit == 0:
            return

        time.sleep(interval)


parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=10)
parser.add_argument('--interval', type=int, default=10)
args = parser.parse_args()

if not os.path.exists('app.db'):
    init_db()

stream_events(args.interval, args.limit)
