from typing import List, Optional

from sqlmodel import Session, select, func

from Models.customer import Customer
from Models.account import Account
from Models.complaint import Complaint
from Models.complaint_status_history import ComplaintStatusHistory
from Models.service_request import ServiceRequest

class customer_repository:
    def __init__(self, session: Session):
        self.session = session
    def get_by_id(self, id):
          return self.session.get(Customer, id)


class account_repository:
    def __init__(self, session: Session):
        self.session = session
    def get_for_customer(self, customer_id: str):
        query = select(Account).where(Account.customer_id == customer_id)
        return self.session.exec(query).all()


class complaint_repository:
    def __init__(self, session: Session):
        self.session = session
    def get_by_id(self, complaint_id: str):
          return self.session.get(Complaint, complaint_id)
    def get_for_complaint(self, customer_id: str):
        query = select(Complaint).where(Complaint.customer_id == customer_id)
        return self.session.exec(query).all()
    def create(self,
        complaint_id: str,
        customer_id: str,
        channel: str,
        category: str,
        description: str,
        priority: str,
        status: str,
        received_at: str,
        assigned_to: str,
        account_id: str):
        complaint = Complaint(complaint_id=complaint_id,
            customer_id=customer_id,
            account_id=account_id,
            channel=channel,
            category=category,
            description=description,
            priority=priority,
            status=status,
            received_at=received_at,
            assigned_to=assigned_to,)
        self.session.add(complaint)
        self.session.commit()
        self.session.refresh(complaint)
        return complaint
    def update_status(self, 
                      complaint_id:str,
                      status: str,
                      date_closed: str = None):
        complaint = self.get_by_id(complaint_id)
        complaint.status = status
        self.session.add(complaint)
        self.session.flush()
        return complaint


class history_repository:
    def __init__(self, session: Session):
        self.session = session
    def get_for_complaint(self, complaint_id):
        query = (
        select(ComplaintStatusHistory)
        .where(ComplaintStatusHistory.complaint_id == complaint_id)
        .order_by(ComplaintStatusHistory.changed_by, ComplaintStatusHistory.history_id)
        )
        return self.session.exec(query).all()
    def next_id(self):
        query = select(func.max(ComplaintStatusHistory.history_id))
        return (self.session.exec(query).one() or 0) + 1
    def add(self,
            complaint_id,
            old_status,
            new_status,
            changed_at,
            changed_by,
            comments):
        history = ComplaintStatusHistory(
            complaint_id=complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            changed_at=changed_at,
            comments=comments
        )
        self.session.add(history)
        self.session.flush()
        return history

class service_request_repository:
    def __init__(self, session: Session):
            self.session = session
    def get_for_complaint(self, complaint_id):
        query = (
            select(ServiceRequest.request_id,
                   ServiceRequest.request_type,
                   ServiceRequest.status,
                   ServiceRequest.created_at)
            .join(Complaint, Complaint.customer_id == ServiceRequest.customer_id)
            .where(Complaint.complaint_id == complaint_id)
            .order_by(ServiceRequest.created_at,
                      ServiceRequest.request_id)
        )
        return self.session.exec(query).all()

        
        



