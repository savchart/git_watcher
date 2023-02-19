from flask import Blueprint, render_template, request

from git_app.models import Event
from git_app.utils import get_events_offset, get_events_counts, calculate_avg_pr_time

events = Blueprint("events", __name__, template_folder="templates")


@events.route("/", methods=["GET"])
def index():
    events_ = Event.query.all()
    events_ = events_[::-1]
    return render_template("index.html", events=events_)


@events.route("/average", methods=["GET", "POST"])
def average():
    if request.method == "POST":
        event_rep = request.form["repository"]
        avg_time = calculate_avg_pr_time(event_rep)
        return render_template("average.html", rep=event_rep, avg_time=avg_time)
    return render_template("average.html")


@events.route("/offset", methods=["GET", "POST"])
def offset():
    if request.method == "POST":
        offset_ = request.form["offset"]
        events_ = get_events_offset(offset_)
        event_counts = get_events_counts(events_)
        return render_template("offset.html", events=event_counts, offset=offset_)
    return render_template("offset.html")


@events.route("/metrics_offset", methods=["GET", "POST"])
def metrics():
    if request.method == "POST":
        offset_ = request.form["offset"]
        events_ = get_events_offset(offset_)
        event_counts = get_events_counts(events_)
        return render_template('visualisation.html', data=event_counts, offset=offset_)
    return render_template('visualisation.html')
