


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
        query = select(func.max(Complaint.complaint_id))
        highest = int(self.session.exec(query).one())
        highest_plus1 = highest + 1
        return "CMP" + format(highest_plus1, "03d")
    
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
        """shouldnt be here should be in service layer"""
        if status == "Closed":
            complaint.date_closed = date_closed
        else:
            None
        self.session.add(complaint)
        self.session.commit()
        self.session.refresh(complaint)
        return complaint
