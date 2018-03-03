# services/flask/project/admin/models.py


from project import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    administrator = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, username, email, administrator=False):
        self.username = username
        self.email = email
        self.administrator = administrator

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'administrator': self.administrator
        }


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    paid_to = db.Column(db.String(64), nullable=False)
    worked_by = db.Column(db.String(64), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    has_paid = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class OneTimeExpense(db.Model):
    __tablename__ = 'one_time_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    paid_by = db.Column(db.String(64), nullable=False)
    tax_category = db.Column(db.String(64), nullable=False)


class RecurringExpense(db.Model):
    __tablename__ = 'recurring_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax_category = db.Column(db.String(64), nullable=False)
    recurrence = db.Column(db.String(64), nullable=False)
    paid_by = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)


