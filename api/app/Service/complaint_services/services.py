"""Complaint service: the business rules the API exposes (Exercises 3.1.2 and 3.3.1). 

  

The service never writes SQL; repositories do. Every method opens ONE 

transaction, so a status change and its history row commit or roll back together. 

  

    service = ComplaintService(DatabaseManager()) 

    service.change_status("CP00001", "In Review", "Picked up for review", role="Analyst") 

""" 

from dataclasses import dataclass 
from datetime import date, datetime, timezone 
from decimal import Decimal 
  

from Repository.account import account_repository
from Repository.complaint import complaint_repository
from Repository.customer import customer_repository
from Repository.history import history_repository
from Repository.service_request import service_request_repository

from domain.errors import ApprovalRequired, ForbiddenRole, InvalidTransition, NotFound 
from domain.models import CLOSABLE, ComplaintStatus, Role, needs_approval, transition_problem, Channel, Category, Priority 

  

@dataclass 
class Repositories: 
    customers: object 
    accounts: object 
    complaints: object 
    history: object 
    requests: object 

def make_repositories(conn): 
    """The real repositories, all on one connection (so one transaction).""" 
    return Repositories(customer_repository(conn), account_repository(conn), complaint_repository(conn), 
                        history_repository(conn), service_request_repository(conn))
  

def audit_event_id_for(history_id): 
    """Week 3 has no audit table: every write adds one history row, that row is the 
    write's audit record, and audit_event_id names it (H00281 -> AUD-000281). 
    Sprint 3's audit log replaces this.""" 
    return f"AUD-{int(history_id[1:]):06d}" 

  

  

class ComplaintService: 
    def __init__(self, session, today=date.today): 
        self.session = session
        self.customers = customer_repository(session)
        self.accounts = account_repository(session)
        self.complaints = complaint_repository(session)
        self.history = history_repository(session)
        self.requests = service_request_repository(session) 
        self.today = today 

    def get_customer(self, customer_id): 
        
        customer = self.customers.get_by_id(customer_id) 
        if customer is None: 
            raise NotFound(f"Customer {customer_id} not found.") 
        return customer 

    def get_accounts(self, customer_id):
        
        customer = self.customers.get_by_id(customer_id) 
        if customer is None: 
            raise NotFound("customer", customer_id)             
        account = self.accounts.get_for_customer(customer_id) 
        return {"customer_id": customer_id, "accounts": account}

    def get_complaint(self, complaint_id):
    
        complaint = self.complaints.get_by_id(complaint_id) 
        history = self.history.get_for_complaint(complaint_id) 
        linked_sr = self.requests.get_for_complaint(complaint_id) 
        return complaint, history, linked_sr

    def change_status(self, complaint_id, target_status, reason, role, actor_id = None):  
        
        complaint = self.complaints.get_by_id(complaint_id) 
        if complaint is None:                 
            raise NotFound(f"complaint {complaint_id} not found.") 

        current = ComplaintStatus(complaint.status)
        target = ComplaintStatus(target_status)
        problem = transition_problem(current, target, Role(role))
        hint = "; use close_complaint."
        if problem == "INVALID_TRANSITION":
            raise InvalidTransition(current.value, target.value, hint)
        if problem == "FORBIDDEN_ROLE":
            raise ForbiddenRole(role, f"Can't move a complaint to {target.value}")

        status = self.complaints.update_status(complaint_id, target) 
        history = self.history.add(complaint_id, current, target, "datetime", actor_id, reason) 
            
        return status, history, audit_event_id_for(history.history_id) 

    def close(self, complaint_id, compensation_cad=Decimal("0"), role="Supervisor", actor_id=None):
        if Role(role) != Role.SUPERVISOR:               
            raise ForbiddenRole(role, "close a complaint")
        
        

        complaint = self.complaints.get_by_id(complaint_id)
        if complaint is None:
            raise NotFound("complaint", complaint_id)

        previous = ComplaintStatus(complaint.status)
        if previous not in CLOSABLE:
            raise InvalidTransition(previous.value, ComplaintStatus.CLOSED.value)

        if needs_approval(Decimal(str(compensation_cad))):
            raise ApprovalRequired(complaint_id, "closing with this compensation")
            
        today = self.today()  
            
        self.complaints.update_status(complaint_id, "Closed", today)
        history = self.history.add(
            complaint_id, previous.value, "Closed",
                datetime.now(timezone.utc), 
            actor_id, "Complaint closed",
        )
        return {
            "complaint_id": complaint_id,
            "previous_status": previous.value,
            "status": "Closed",
            "date_closed": today,
            "closed_by": actor_id,
            "approval_id": None,
            "audit_event_id": audit_event_id_for(history.history_id),
        }

    def create(self, customer_id, channel, category, complaint_text,
               priority, account_id=None,
               assigned_analyst_id=None):

        today = self.today()

        channel = Channel(channel).value
        category = Category(category).value
        priority = Priority(priority).value

        complaint = self.complaints.create(
            complaint_id=self.complaints.next_id(),
            customer_id=customer_id,
            account_id=account_id,
            channel=channel,
            category=category,
            complaint_text=complaint_text,
            priority=priority,
            status=ComplaintStatus.OPEN.value,
            received_at=today,
            assigned_analyst_id=assigned_analyst_id,
        )


    # TODO get_accounts, get_complaint (+ _complaint_with_children), change_status, 
    #      close 


def _v(value): 
    """Enum member or plain string -> plain string.""" 
    return getattr(value, "value", value)

