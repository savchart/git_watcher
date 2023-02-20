from datetime import datetime, timedelta
from git_app.models import Event


def get_events_offset(offset_minutes):
    offset_time = datetime.utcnow() - timedelta(minutes=int(offset_minutes))
    return Event.query.filter(Event.created_at >= offset_time).all()


def get_events_counts(events):
    event_counts = {et: 0 for et in ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']}
    for event in events:
        event_counts[event.event_type] += 1
    return event_counts


def calculate_avg_pr_time(repository):
    pull_requests = Event.query.filter_by(event_type='PullRequestEvent',
                                          repository=repository).order_by(Event.created_at.asc()).all()
    if not pull_requests:
        return None
    total_time = 0
    num_prs = len(pull_requests)
    for i in range(num_prs - 1):
        pr1 = pull_requests[i]
        pr2 = pull_requests[i + 1]
        total_time += (pr2.created_at - pr1.created_at).total_seconds()
    return total_time / (num_prs - 1)
