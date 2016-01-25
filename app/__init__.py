import os

from flask import Flask, render_template, request
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter

# from settings import DevConfig as config

app = Flask(
    __name__,
    # template_folder=config.TEMPLATE_DIR,
)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
admin = Admin(app)

from app.mod_site.controllers import mod_site
app.register_blueprint(mod_site)

from app.mod_user.controllers import mod_user
app.register_blueprint(mod_user)

from app.mod_movie.controllers import mod_movie
app.register_blueprint(mod_movie)

from app.mod_user.models import User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

from app.mod_admin import init_admin
init_admin(admin)
