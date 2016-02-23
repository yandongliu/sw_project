import os

from flask import Blueprint, request, render_template
from flask_user import current_user, login_required
from werkzeug import secure_filename

from app import app
from app.mod_movie.models import Movie

mod_site = Blueprint('site', __name__, url_prefix='/')

@mod_site.route('/', methods=['GET'])
def index():
    movies =  Movie.get_all_movies()
    m = movies[0]
    # import pdb; pdb.set_trace()
    return render_template("site/index.html", movies=movies)
