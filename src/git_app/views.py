from flask import Blueprint, render_template
from git_app.models import Event

events = Blueprint("events", __name__, template_folder="templates")


@events.route("/", methods=["GET"])
def index():
    events_ = Event.query.all()
    events_ = events_[::-1]
    return render_template("index.html", events=events_)
