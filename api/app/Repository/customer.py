from sqlmodel import Session

from Models.customer import Customer


class customer_repository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id):
          return self.session.get(Customer, id)

