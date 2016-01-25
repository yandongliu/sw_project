from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.user.signals import user_logged_in, user_registered
from flask_user import current_user, login_required

import app

from app import db
from models import User

mod_user = Blueprint('user', __name__, url_prefix='/user')

@mod_user.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Setting saved.')
        return redirect(url_for('.dashboard'))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone.data = current_user.phone
    form.address.data = current_user.address
    form.city.data = City.get_name_by_id(current_user.city_id)
    form.country_id.data = Country.get_name_by_id(
        current_user.country_id)
    form.zipcode.data = current_user.zipcode
    return render_template("user/dashboard.html", form=form)

@mod_user.route('/update', methods=['POST'])
@login_required
def update_user():
    form = UserForm()
    if form.validate_on_submit():
        print form
    return 'hi'

@mod_user.route('/')
def show_users():
    users = User.query.all()
    return render_template("user/index.html", users=users)

@mod_user.route('/profile')
@login_required
def user_profile():
    return 'hi'

@mod_user.route('/setting')
@login_required
def setting():
    return 'setting'

# seems the hook doesn't work if placed here
@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    sender.logger.info('user logged in')
    print 'mod_user controller: user logged in'

