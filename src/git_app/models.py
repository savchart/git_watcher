from git_app.extensions import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    repository = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, event_type, repository, created_at):
        self.event_type = event_type
        self.repository = repository
        self.created_at = created_at

    def __repr__(self):
        return f"{self.event_type} | {self.repository} | {self.created_at}"


