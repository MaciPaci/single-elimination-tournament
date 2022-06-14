from flask import Blueprint, render_template, redirect, url_for, request, flash
import uuid
import random
from . import db
from .models import Tournament, Player, Match
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
    phase = request.args.get('phase')
    if not phase:
        phase = "1"
    player_list = Player.query.filter_by(tournament_id=tournament_id)
    match_list = Match.query.filter_by(tournament_id=tournament_id, phase=phase)
    grouped_matches = Match.query.filter_by(tournament_id=tournament_id).group_by('phase').all()
    phases = [0]
    for match in grouped_matches:
        phases.append(int(match.phase))
    tournament = Tournament.query.filter_by(tournament_id=tournament_id).first()
    winner = tournament.winner
    return render_template('tournament_manage.html', tournament_id=tournament_id, list_of_players=player_list,
                           list_of_matches=match_list, phases=phases, phase=phase, winner=winner)


@tournament.route('/tournament/<string:tournament_id>', methods=['POST'])
@login_required
def manage_post(tournament_id):
    name = request.form.get('name')

    if name == "":
        flash('Please fill all fields.')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    players = Player.query.filter_by(tournament_id=tournament_id).all()
    tournament = Tournament.query.filter_by(tournament_id=tournament_id).first()
    if len(players) >= int(tournament.player_count):
        flash('Maximum number of players reached')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    player = Player.query.filter_by(name=name, tournament_id=tournament_id).first()

    if player:
        flash('Player already enrolled into the tournament')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    new_player = Player(tournament_id=tournament_id, name=name)

    db.session.add(new_player)
    db.session.commit()

    player_list = Player.query.filter_by(tournament_id=tournament_id)

    return redirect(url_for('tournament.manage', tournament_id=tournament_id, list_of_players=player_list))


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
    Player.query.filter_by(tournament_id=tournament_id).delete()
    db.session.commit()
    return redirect(url_for('tournament.list'))


@tournament.route('/tournament/<string:tournament_id>/bracket/generate')
def generate_bracket(tournament_id):
    bracket = Match.query.filter_by(tournament_id=tournament_id).all()
    if bracket:
        flash('Bracket already generated')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    player_list = Player.query.filter_by(tournament_id=tournament_id).all()
    tournament = Tournament.query.filter_by(tournament_id=tournament_id).first()

    if len(player_list) < int(tournament.player_count):
        flash('Please fill out all the players before generating the bracket')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id))

    random.shuffle(player_list)
    half = len(player_list) // 2
    pool1, pool2 = player_list[:half], player_list[half:]
    for (player1, player2) in zip(pool1, pool2):
        new_match = Match(id=uuid.uuid4().hex, tournament_id=tournament_id, player1_name=player1.name,
                          player2_name=player2.name, player1_score=0, player2_score=0, phase=1)
        db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('tournament.manage', tournament_id=tournament_id))


@tournament.route('/tournament/<string:tournament_id>/score/save/<string:match_id>/<string:phase>', methods=['POST'])
def save_score(tournament_id, match_id, phase):
    score1 = request.form.get('score1')
    score2 = request.form.get('score2')

    if score1 == "":
        score1 = "0"
    if score2 == "":
        score2 = "0"

    match = Match.query.filter_by(id=match_id).first()
    match.player1_score = int(score1)
    match.player2_score = int(score2)

    db.session.commit()

    return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=phase))


@tournament.route('/tournament/<string:tournament_id>/phase/<int:phase>')
def generate_next_phase(tournament_id, phase):
    if phase == 0:
        flash('This is a final phase')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=0))
    matches = Match.query.filter_by(tournament_id=tournament_id, phase=phase).all()

    next_phase = phase + 1
    players = []

    if not matches:
        flash('Generate bracket first')
        return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=next_phase))

    for match in matches:
        if match.player1_score == 0 and match.player2_score == 0:
            flash('Cannot determine a winner. Resolve all drawn matches')
            return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=next_phase))
        if match.player1_score > match.player2_score:
            player = Player.query.filter_by(name=match.player1_name).first()
            players.append(player)
        else:
            player = Player.query.filter_by(name=match.player2_name).first()
            players.append(player)

    if len(players) == 1:
        tournament = Tournament.query.filter_by(tournament_id=tournament_id).first()
        tournament.winner = players[0].name
        db.session.commit()
        return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=0))

    random.shuffle(players)
    half = len(players) // 2
    pool1, pool2 = players[:half], players[half:]
    for (player1, player2) in zip(pool1, pool2):
        new_match = Match(id=uuid.uuid4().hex, tournament_id=tournament_id, player1_name=player1.name,
                          player2_name=player2.name, player1_score=0, player2_score=0, phase=next_phase)
        db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('tournament.manage', tournament_id=tournament_id, phase=next_phase))
