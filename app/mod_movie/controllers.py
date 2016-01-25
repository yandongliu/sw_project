from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.user.signals import user_logged_in, user_registered
from flask_user import current_user, login_required

import app

from app import db
from models import Movie

mod_movie = Blueprint('movie', __name__, url_prefix='/movie')


@mod_movie.route('/recommendation')
def recommendation():
    return render_template("movie/recommendation.html", movies=[])
