import os
import time
from .. import celery
from ..models import db, USSD_Transactions, STATUS_CHOICES


@celery.task
def add_transaction(id):
    ussd_trans = USSD_Transactions.query.get(
        USSD_Transactions.id=id
    )
    ussd_trans.status = STATUS_CHOICES.failed
    db.session.commit()
    return True