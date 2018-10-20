import json

from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app import db
from app.models import Anime, Episode, UserRatedEpisodes

# Define the blueprint: 'anime_mod', set its url prefix: app.url/
anime_mod = Blueprint('anime_mod', __name__, url_prefix='/')


@anime_mod.route('/animes')
def animes():
	animes = Anime.query.order_by(Anime.id).limit(10).all()
	return render_template('anime/index.html', title='Animes', animes=animes)


@anime_mod.route('/a/<int:id>')
def anime_details(id: int):
	anime = Anime.query.get_or_404(id)
	categories = ", ".join([x.name for x in anime.genres])
	return render_template('anime/anime_detail.html', title=anime.name, anime=anime, categories=categories)


@anime_mod.route('/v/<int:id>')
def episode(id: int):
	episode = Episode.query.get_or_404(id)
	next_epis = Episode.query.filter(Episode.number > episode.number).limit(10).all()
	anterior = Episode.query.filter(Episode.number < episode.number).order_by(Episode.number).first()

	rate = None
	if current_user.is_authenticated:
		rate = current_user.rated_episodes.filter_by(episode_id=id).first()
	like = rate.liked if rate else False
	dislike = rate.disliked if rate else False

	return render_template('anime/episode_detail.html', title=episode.__str__(), episode=episode, next=next_epis, before=anterior, liked=like, disliked=dislike)


@login_required
@anime_mod.route('/like/<int:id>', methods=['GET'])
def like_episode(id: int):
	if not current_user.is_authenticated:
		return json.dumps(""), 401, {'ContentType': 'application/json'}

	row = current_user.rated_episodes.filter_by(episode_id=id).first()

	# Row doesn't exist in DB
	if not row:
		obj = UserRatedEpisodes(user_id=current_user.id, episode_id=id, liked=True, disliked=False)
		current_user.rated_episodes.append(obj)
		db.session.commit()
		return json.dumps({'success': True, 'liked': True, 'disliked': False}), 200, {'ContentType': 'application/json'}

	# Row exists in db
	else:
		row.liked = liked = not row.liked
		row.disliked = False
		db.session.commit()
		return json.dumps({'success': True, 'liked': liked, 'disliked': False}), 200, {'ContentType': 'application/json'}


@login_required
@anime_mod.route('/dislike/<int:id>', methods=['GET'])
def dislike_episode(id: int):
	if not current_user.is_authenticated:
		return json.dumps(""), 401, {'ContentType': 'application/json'}

	row = current_user.rated_episodes.filter_by(episode_id=id).first()

	# Row doesn't exist in DB
	if not row:
		obj = UserRatedEpisodes(user_id=current_user.id, episode_id=id, liked=False, disliked=True)
		current_user.rated_episodes.append(obj)
		db.session.commit()
		return json.dumps({'success': True, 'disliked': True, 'liked': False}), 200, {'ContentType': 'application/json'}

	# Row exists in db
	else:
		row.liked = False
		row.disliked = disliked = not row.disliked
		db.session.commit()
		return json.dumps({'success': True, 'disliked': disliked, 'liked': False}), 200, {'ContentType': 'application/json'}
