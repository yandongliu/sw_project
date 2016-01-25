from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask_user import current_user

from app import db
from app.mod_user.models import User

class MyView(BaseView):
    def is_accessible(self):
        # return current_user.is_admin()
        return True

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class MyModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        # import pdb; pdb.set_trace()
        return True
        # if not current_user.is_authenticated: return False
        # return current_user.has_roles('admin')

def init_admin(_admin):
    _admin.add_view(MyView(name='Hello'))
    _admin.add_view(MyModelView(User, db.session, endpoint='admin_user'))
