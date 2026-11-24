


from sqlmodel import Session, select, func
from Models.complaint import Complaint

class complaint_repository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, complaint_id: str):
          return self.session.get(Complaint, complaint_id)
    
    def get_for_complaint(self, customer_id: str):
        query = select(Complaint).where(Complaint.customer_id == customer_id)
        return self.session.exec(query).all()

    def next_id(self):
        highest = self.session.exec(select(func.max(Complaint.complaint_id))).one()
        number = int(highest[3:]) + 1 
        return f"CMP{number:03d}"
    
    def create(self,
        complaint_id: str,
        customer_id: str,
        channel: str,
        category: str,
        complaint_text: str,
        priority: str,
        status: str,
        received_at: str,
        assigned_analyst_id: str = None,
        account_id: str = None):
        complaint = Complaint(complaint_id=complaint_id,
            customer_id=customer_id,
            account_id=account_id,
            channel=channel,
            category=category,
            complaint_text=complaint_text,
            priority=priority,
            status=status,
            received_at=received_at,
            assigned_analyst_id=assigned_analyst_id,)
        self.session.add(complaint)
        self.session.commit()
        self.session.refresh(complaint)
        return complaint
    
    def update_status(self, 
                      complaint_id:str,
                      status: str,
                      ):
        complaint = self.get_by_id(complaint_id)
        complaint.status = status
        self.session.add(complaint)
        self.session.commit()
        self.session.refresh(complaint)
        return complaint
