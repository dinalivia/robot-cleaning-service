from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Execution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    commands = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float, nullable=False)
