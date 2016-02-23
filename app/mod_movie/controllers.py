from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.user.signals import user_logged_in, user_registered
from flask_user import current_user, login_required

import app

from app import cache, db
from models import Movie

mod_movie = Blueprint('movie', __name__, url_prefix='/movie')


@mod_movie.route('/recommendation')
def recommendation():
    movies = Movie.get_all_movies()
    return render_template("movie/recommendation.html", movies=movies)

@cache.cached(timeout=50)
@mod_movie.route('/<int:id>')
def index(id):
    # import pdb; pdb.set_trace()
    # id = request.args.get('id')
    movie = Movie.query.get(id)
    return render_template("movie/recommendation.html", movies=[movie])
