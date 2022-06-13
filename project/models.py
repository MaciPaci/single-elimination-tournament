from flask_login import UserMixin
from sqlalchemy import Integer

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    start_date = db.Column(db.String(100))
    player_count = db.Column(db.String(10))


class Player(db.Model):
    tournament_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(1000), primary_key=True)


class Match(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    tournament_id = db.Column(db.String(100))
    player1_name = db.Column(db.String(1000))
    player2_name = db.Column(db.String(1000))
    player1_result = db.Column(db.Integer)
    player2_result = db.Column(db.Integer)
