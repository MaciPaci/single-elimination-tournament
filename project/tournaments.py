from flask import Blueprint, render_template, redirect, url_for, request
import uuid
from . import db
from .models import Tournament
from flask_login import login_required

tournament = Blueprint('tournament', __name__)


@tournament.route('/tournament/create')
@login_required
def create_tournament():
    return render_template('tournament_create.html')


@tournament.route('/tournament/create', methods=['POST'])
@login_required
def create_tournament_post():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    player_count = request.form.get('player_count')
    id = uuid.uuid4().hex

    new_tournament = Tournament(tournament_id=id, name=name, start_date=start_date, player_count=player_count)

    db.session.add(new_tournament)
    db.session.commit()

    return redirect(url_for('tournament.manage_tournament', tournament_id=id))


@tournament.route('/tournament/<string:tournament_id>')
@login_required
def manage_tournament(tournament_id):
    return render_template('tournament_manage.html', tournament_id=tournament_id)


@tournament.route('/tournament/list')
def list_tournament():
    tournaments_list = Tournament.query.all()
    return render_template('tournament_list.html', list_of_tournaments=tournaments_list)
