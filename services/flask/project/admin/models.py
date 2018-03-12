# services/flask/project/admin/models.py

import enum
import datetime
import jwt

from flask import current_app

from project import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
                password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.is_admin = is_admin

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            exp_days = current_app.config.get('TOKEN_EXPIRATION_DAYS')
            exp_seconds = current_app.config.get('TOKEN_EXPIRATION_SECONDS')
            exp = (datetime.datetime.utcnow() +
                   datetime.timedelta(exp_days, exp_seconds))
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token - :param auth_token: - :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Job(db.Model):

    class PaidTo(enum.Enum):
        GLADTIMEAUDIO = 'Gladtime Audio'
        MEGHAN = 'Meghan'
        TYLER = 'Tyler'
        TMSEPARATELY = 'Tyler/Meghan Separately'

    class WorkedBy(enum.Enum):
        MEGHAN = 'Meghan'
        TYLER = 'Tyler'
        TYLER_AND_MEGHAN = 'Tyler and Meghan'

    class Confirmation(enum.Enum):
        CONFIRMED = 'Confirmed'
        PENCILLED_IN = 'Pencilled In'

    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    paid_to = db.Column(db.Enum(PaidTo), nullable=False)
    worked_by = db.Column(db.Enum(WorkedBy), nullable=False)
    confirmation = db.Column(db.Enum(Confirmation), nullable=False)
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
        self.paid_to = self.PaidTo(paid_to)
        self.worked_by = self.WorkedBy(worked_by)
        self.confirmation = self.Confirmation(confirmation)
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

    class PaidBy(enum.Enum):
        TYLER_AND_MEGHAN = 'Tyler and Meghan'
        TYLER = 'Tyler'
        MEGHAN = 'Meghan'

    class Category(enum.Enum):
        BUSINESS_EQUIPMENT = 'Business Equipment'
        BUSINESS_SUPPLIES = 'Business Supplies'
        GASOLINE = 'Gasoline'
        VEHICLE_MAINTENANCE = 'Vehicle Maintenance'
        TRAVEL_EXPENSE = 'Travel Expense'
        ENTERTAINMENT = 'Entertainment'
        FOOD = 'Food'

    __tablename__ = 'one_time_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount_spent = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    paid_by = db.Column(db.Enum(PaidBy, name='paidby_one_time_expense'),
                        nullable=False)
    tax_deductible = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.Enum(Category, name='category_one_time_expense'),
                         nullable=False)

    def __init__(self, merchant, description, amount_spent, date, paid_by,
                 tax_deductible, category):
        self.merchant = merchant
        self.description = description
        self.amount_spent = amount_spent
        self.date = date
        self.paid_by = self.PaidBy(paid_by)
        self.tax_deductible = tax_deductible
        self.category = self.Category(category)

    def to_json(self):
        return {
            'id': self.id,
            'merchant': self.merchant,
            'description': self.description,
            'amount_spent': self.amount_spent,
            'date': self.date.isoformat(),
            'paid_by': self.paid_by.value,
            'tax_deductible': self.tax_deductible,
            'category': self.category.value,
        }


class RecurringExpense(db.Model):

    class Category(enum.Enum):
        HOUSING = 'Housing'
        ENTERTAINMENT = 'Entertainment'
        UTILITIES = 'Utilities'
        OTHER = 'Other'

    class Recurrence(enum.Enum):
        MONTHLY = 'Monthly'
        EVERY_OTHER_MONTH = 'Every Other Month'
        EVERY_SIX_MONTHS = 'Every Six Months'
        ONCE_PER_YEAR = 'Once Per Year'

    class PaidBy(enum.Enum):
        TYLER_AND_MEGHAN = 'Tyler and Meghan'
        TYLER = 'Tyler'
        MEGHAN = 'Meghan'

    __tablename__ = 'recurring_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax_deductible = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.Enum(Category, name='category_recurring_expense'),
                         nullable=False)
    recurrence = db.Column(db.Enum(Recurrence), nullable=False)
    paid_by = db.Column(db.Enum(PaidBy, name='paid_by_recurring_expense'),
                        nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    __table_args__ = (
            db.CheckConstraint('end_date >= start_date OR end_date IS NULL',
                               name='check_dates_recurring_expense'),
            {})

    def __init__(self, merchant, description, amount, tax_deductible,
                 category, recurrence, paid_by, start_date, end_date=None):
        self.merchant = merchant
        self.description = description
        self.amount = amount
        self.tax_deductible = tax_deductible
        self.category = self.Category(category)
        self.recurrence = self.Recurrence(recurrence)
        self.paid_by = self.PaidBy(paid_by)
        self.start_date = start_date
        self.end_date = end_date

    def to_json(self):
        json_object = {
            'id': self.id,
            'merchant': self.merchant,
            'description': self.description,
            'amount': self.amount,
            'tax_deductible': self.tax_deductible,
            'category': self.category.value,
            'recurrence': self.recurrence.value,
            'paid_by': self.paid_by.value,
            'start_date': self.start_date.isoformat(),
        }
        if self.end_date:
            json_object['end_date'] = self.end_date.isoformat()
        return json_object
