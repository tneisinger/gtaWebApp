# services/flask/project/tests/utils.py


from project import db
from project.admin.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user
