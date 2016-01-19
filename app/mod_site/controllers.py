import os

from flask import Blueprint, request, render_template
from werkzeug import secure_filename

from app import app

mod_site = Blueprint('site', __name__, url_prefix='/')

@mod_site.route('/', methods=['GET'])
def index():
    return render_template("site/index.html")
