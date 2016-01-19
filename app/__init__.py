import os

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

# from settings import DevConfig as config

app = Flask(
    __name__,
    # template_folder=config.TEMPLATE_DIR,
)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from app.mod_site.controllers import mod_site
app.register_blueprint(mod_site)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
