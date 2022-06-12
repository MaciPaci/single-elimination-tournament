from flask import Blueprint, render_template, redirect, url_for, request, flash
import uuid
from . import db
from .models import Tournament, Player
from flask_login import login_required

tournament = Blueprint('tournament', __name__)


@tournament.route('/tournament/create')
@login_required
def create():
    return render_template('tournament_create.html')


@tournament.route('/tournament/create', methods=['POST'])
@login_required
def create_post():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    player_count = request.form.get('player_count')

    if name == "" or start_date == "":
        flash('Please fill all fields.')
        return redirect(url_for('tournament.create'))

    id = uuid.uuid4().hex

    new_tournament = Tournament(tournament_id=id, name=name, start_date=start_date, player_count=player_count)

    db.session.add(new_tournament)
    db.session.commit()

    return redirect(url_for('tournament.manage', tournament_id=id))


@tournament.route('/tournament/<string:tournament_id>')
@login_required
def manage(tournament_id):
    player_list = Player.query.all()
    return render_template('tournament_manage.html', tournament_id=tournament_id, list_of_players=player_list)


@tournament.route('/tournament/<string:tournament_id>', methods=['POST'])
@login_required
def manage_post(tournament_id):
    name = request.form.get('name')

    if name == "":
        flash('Please fill all fields.')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    player = Player.query.filter_by(name=name, tournament_id=tournament_id).first()

    if player:
        flash('Player already enrolled into the tournament')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    new_player = Player(tournament_id=tournament_id, name=name)

    db.session.add(new_player)
    db.session.commit()

    player_list = Player.query.all()

    return render_template('tournament_manage.html', tournament_id=tournament_id, list_of_players=player_list)


@tournament.route('/tournament/<string:tournament_id>/<string:name>')
@login_required
def manage_delete(tournament_id, name):
    Player.query.filter_by(tournament_id=tournament_id, name=name).delete()
    db.session.commit()
    return redirect(url_for('tournament.manage', tournament_id=tournament_id))

@tournament.route('/tournament/list')
def list():
    if request.form.get("manage_button"):
        print(request.form.get("manage_button"))
    tournaments_list = Tournament.query.all()
    return render_template('tournament_list.html', list_of_tournaments=tournaments_list)


@tournament.route('/tournament/remove/<string:tournament_id>')
def remove(tournament_id):
    Tournament.query.filter_by(tournament_id=tournament_id).delete()
    db.session.commit()
    return redirect(url_for('tournament.list'))
