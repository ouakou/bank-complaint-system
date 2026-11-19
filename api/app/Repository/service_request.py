
from sqlmodel import Session, select

from Models.complaint import Complaint
from Models.service_request import ServiceRequest


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

        
        
