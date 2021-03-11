import enum
from datetime import datetime

from . import db


class STATUS_CHOICES(enum.Enum):
    failed = "failed"
    pending = "pending"
    success = "success"


class USSD_Transactions(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    merchant_id = db.Column(db.String(120), index=True, nullable=False)
    amount = db.Column(db.Float, index=True, nullable=False)
    refCode = db.Column(db.Unicode, index=True, nullable=False)
    status = db.Column(
        db.Enum(STATUS_CHOICES), default=STATUS_CHOICES.pending, nullable=False
    )

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.merchant_id}>"
