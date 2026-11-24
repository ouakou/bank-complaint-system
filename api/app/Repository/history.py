

from sqlmodel import Session, select, func
from Models.complaint_status_history import ComplaintStatusHistory

class history_repository:
    def __init__(self, session: Session):
        self.session = session

    def get_for_complaint(self, complaint_id):
        query = (
        select(ComplaintStatusHistory)
        .where(ComplaintStatusHistory.complaint_id == complaint_id)
        .order_by(ComplaintStatusHistory.changed_at, ComplaintStatusHistory.history_id)
        )
        return self.session.exec(query).all()
    
    def next_id(self):
        query = select(func.max(ComplaintStatusHistory.history_id))
        highest = int(self.session.exec(query).one())
        highest_plus1 = highest + 1
        return "H" + format(highest_plus1, "05d")
    
    def add(self,
            complaint_id,
            old_status,
            new_status,
            changed_at,
            changed_by_role,
            comments):
        #history_id = self.next_id()
        history = ComplaintStatusHistory(
            #history_id=history_id,
            complaint_id=complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by_role,
            changed_at=changed_at,
            comments = comments,
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history