# services/flask/project/admin/models.py


import enum

from project import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
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


class JobPaidToOption(enum.Enum):
    GLADTIMEAUDIO = 'Gladtime Audio'
    MEGHAN = 'Meghan'
    TYLER = 'Tyler'
    TMSEPARATELY = 'Tyler/Meghan Separately'


class JobWorkedByOption(enum.Enum):
    MEGHAN = 'Meghan'
    TYLER = 'Tyler'
    TYLER_AND_MEGHAN = 'Tyler and Meghan'


class JobConfirmationOption(enum.Enum):
    CONFIRMED = 'Confirmed'
    PENCILLED_IN = 'Pencilled In'


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    paid_to = db.Column(db.Enum(JobPaidToOption), nullable=False)
    worked_by = db.Column(db.Enum(JobWorkedByOption), nullable=False)
    confirmation = db.Column(db.Enum(JobConfirmationOption), nullable=False)
    has_paid = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    __table_args__ = (
            db.CheckConstraint('end_date >= start_date', name='check_dates'),
            {})

    def __init__(self, client, description, amount_paid, paid_to, worked_by,
                 confirmation, has_paid, start_date, end_date=None):
        self.client = client
        self.description = description
        self.amount_paid = amount_paid
        self.paid_to = JobPaidToOption(paid_to)
        self.worked_by = JobWorkedByOption(worked_by)
        self.confirmation = JobConfirmationOption(confirmation)
        self.has_paid = has_paid
        self.start_date = start_date
        if end_date:
            self.end_date = end_date
        else:
            self.end_date = start_date

    def to_json(self):
        return {
            'id': self.id,
            'client': self.client,
            'description': self.description,
            'amount_paid': self.amount_paid,
            'paid_to': self.paid_to.value,
            'worked_by': self.worked_by.value,
            'confirmation': self.confirmation.value,
            'has_paid': self.has_paid,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        }


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
