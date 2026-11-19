
from sqlmodel import Session, select

from Models.account import Account
class account_repository:
    def __init__(self, session: Session):
        self.session = session

    def get_for_customer(self, customer_id: str):
        query = select(Account).where(Account.customer_id == customer_id)
        return self.session.exec(query).all()