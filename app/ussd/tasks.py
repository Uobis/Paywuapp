from .. import celery
from ..models import STATUS_CHOICES, USSD_Transactions, db


@celery.task
def add_transaction(id):
    ussd_trans = USSD_Transactions.query.get(id)
    ussd_trans.status = STATUS_CHOICES.failed
    db.session.commit()
    return True
