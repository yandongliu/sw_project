from datetime import datetime
import os
from random import choice

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db, user_manager
from app.mod_user.models import User, Role

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('migrate', MigrateCommand)

@manager.command
def create_tables():
    """create all tables"""
    # db.reflect()
    db.create_all()

@manager.command
def drop_tables():
    """drop all tables"""
    db.reflect()
    db.drop_all()

@manager.command
def create_data():
    """populate db with initial data"""
    role1 = Role(name='user')
    role2 = Role(name='admin')

    for i in xrange(1, 6):
        _user = User(
            username='user%d' % i,
            email='user%d@example.com' % i,
            is_enabled=True,
            active=True,
            first_name=random_name(),
            last_name=random_name(),
            password=user_manager.hash_password('Password1'),
            confirmed_at=datetime.utcnow(),
        )
        _user.roles.append(role1)
        db.session.add(_user)
    db.session.commit()

@manager.command
def delete_data():
    """empty all tables"""
    db.session.execute('delete from "user"')
    db.session.execute('delete from "role"')
    db.session.commit()

@manager.command
def test():
    """unit test"""
    print 'unit test'

@manager.command
def allusers():
    for u in User.query.all():
        print u.email

names = ['john', 'daniel', 'eric', 'steve', 'peter']
def random_name():
    return choice(names)

if __name__ == '__main__':
    manager.run()
