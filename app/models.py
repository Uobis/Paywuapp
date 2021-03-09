from flask_login import UserMixin
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, random, datetime, time
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(120), index=True, nullable=False)
    last_name = db.Column(db.String(120), index=True, nullable=False)
    email = db.Column(db.Unicode, index=True, unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True)

    password_hash = db.Column(db.String(128))

    business_name = db.Column(db.String())
    is_company = db.Column(db.Boolean, default=False)

    bank_account = db.relationship("BankDetails", backref="owner", lazy="dynamic")
    wallet = db.relationship("Wallet", backref="owner", lazy="dynamic")

    accept_terms = db.Column(db.Boolean)

    is_active = db.Column(db.Boolean, default=False)
    joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password(self, expires_in=600):
        return jwt.encode(
            {"resetpassword": self.id, "exp": time.time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f"<User {self.email}>"


class BankDetails(db.Model):
    __tablename__ = "bank_details"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    account_number = db.Column(db.String)
    account_name = db.Column(db.String)
    bank = db.Column(db.String)
    bank_id = db.Column(db.String)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Wallet(db.Model):
    __tablename__ = "wallets"

    balance = db.Column(db.REAL, default=0)
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    prev_balance = db.Column(db.REAL, default=0)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def repr(self):
        return self.owner_id

    def increment(self, value):
        self.prev_balance = self.balance
        self.balance = self.balance + float(value)
        self.updated = datetime.datetime.utcnow()
        return True

    def decrease(self, value):
        self.prev_balance = self.balance

        """
         1. Check that the guy is not a merchant
         2. if merchant, just check that their amount to deduct is <= the balance
         3. Else use the percentage to calculate how much they can withdraw 
         4. return of false means insufficient balance 
        """
        check = self.balance - float(value)
        if check > 0:
            self.balance = self.balance - float(value)
            self.updated = datetime.datetime.utcnow()
            return True
        else:
            return False

    def can_withdraw(self, value):
        if self.balance > float(value):
            return True
        else:
            return False

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class LogsInternal(db.Model):
#     __tablename__ = "logs_internal"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String)
#     event = db.Column(db.String)
#     amount = db.Column(db.REAL)
#     time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class LogsExternal(db.Model):
#     __tablename__ = "logs_external"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     other_id = db.Column(db.Integer)
#     event = db.Column(db.String)
#     event_type = db.Column(db.String)
#     amount = db.Column(db.REAL)
#     time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class AdminAccounts(db.Model):
#     __tablename__ = "admins"
#     id = db.Column(db.Integer, primary_key=True)
#     created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#     email = db.Column(db.String)
#     password_hash = db.Column(db.String)

#     @property
#     def password(self):
#         return "password is not readable"

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    contact_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner_id = db.Column(db.Integer)


class Voucher(db.Model):
    __tablename__ = "vouchers"
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String)
    amount = db.Column(db.REAL)
    code = db.Column(db.String, unique=True)
    used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
