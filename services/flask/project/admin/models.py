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


class OneTimeExpensePaidByOption(enum.Enum):
    TYLER_AND_MEGHAN = 'Tyler and Meghan'
    TYLER = 'Tyler'
    MEGHAN = 'Meghan'


class OneTimeExpenseCategoryOption(enum.Enum):
    BUSINESS_EQUIPMENT = 'Business Equipment'
    BUSINESS_SUPPLIES = 'Business Supplies'
    GASOLINE = 'Gasoline'
    VEHICLE_MAINTENANCE = 'Vehicle Maintenance'
    TRAVEL_EXPENSE = 'Travel Expense'
    ENTERTAINMENT = 'Entertainment'
    FOOD = 'Food'


class OneTimeExpense(db.Model):
    __tablename__ = 'one_time_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount_spent = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    paid_by = db.Column(db.Enum(OneTimeExpensePaidByOption), nullable=False)
    tax_deductible = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.Enum(OneTimeExpenseCategoryOption), nullable=False)

    def __init__(self, merchant, description, amount_spent, date, paid_by,
                 tax_deductible, category):
        self.merchant = merchant
        self.description = description
        self.amount_spent = amount_spent
        self.date = date
        self.paid_by = OneTimeExpensePaidByOption(paid_by)
        self.tax_deductible = tax_deductible
        self.category = OneTimeExpenseCategoryOption(category)

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

    class CategoryOption(enum.Enum):
        HOUSING = 'Housing'
        ENTERTAINMENT = 'Entertainment'
        UTILITIES = 'Utilities'
        OTHER = 'Other'

    class RecurrenceOption(enum.Enum):
        MONTHLY = 'Monthly'
        EVERY_OTHER_MONTH = 'Every Other Month'
        EVERY_SIX_MONTHS = 'Every Six Months'
        ONCE_PER_YEAR = 'Once Per Year'

    class PaidByOption(enum.Enum):
        TYLER_AND_MEGHAN = 'Tyler and Meghan'
        TYLER = 'Tyler'
        MEGHAN = 'Meghan'

    __tablename__ = 'recurring_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_deductible = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.Enum(CategoryOption), nullable=False)
    recurrence = db.Column(db.Enum(RecurrenceOption), nullable=False)
    paid_by = db.Column(db.Enum(PaidByOption), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    def __init__(self, merchant, description, amount, is_deductible,
                 category, recurrence, paid_by, start_date, end_date=None):
        self.merchant = merchant
        self.description = description
        self.amount = amount
        self.is_deductible = is_deductible
        self.category = self.CategoryOption(category)
        self.recurrence = self.RecurrenceOption(recurrence)
        self.paid_by = self.PaidByOption(paid_by)
        self.start_date = start_date
        self.end_date = end_date
