from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    start_date = db.Column(db.String(100))
    player_count = db.Column(db.String(10))
    winner = db.Column(db.String(1000))
    owner = db.Column(db.Integer)


class Player(db.Model):
    tournament_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(1000), primary_key=True)


class Match(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    tournament_id = db.Column(db.String(100))
    player1_name = db.Column(db.String(1000))
    player2_name = db.Column(db.String(1000))
    player1_score = db.Column(db.Integer)
    player2_score = db.Column(db.Integer)
    phase = db.Column(db.Integer)
