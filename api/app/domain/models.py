from enum import Enum
from decimal import Decimal
class ComplaintStatus(str, Enum): 

    OPEN = "Open" 
    IN_REVIEW = "In Review" 
    PENDING_APPROVAL = "Pending Approval" 
    ESCALATED = "Escalated" 
    CLOSED = "Closed" 


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Channel(str, Enum):
    PHONE = "Phone"
    WEB = "Web"
    EMAIL = "Email"
    BRANCH = "Branch"

class Category(str, Enum):
    FEE = "Fee"
    CARD = "Card" 
    TRANSACTION_DISPUTE = "Transaction Dispute"
    DIGITAL_BANKING = "Digital Banking"
    SERVICE_QUALITY = "Service Quality"
    MORTGAGE_SERVICES = "Mortgage Servicing"
    ACCOUNT_ACCESS = "Account Access"


class Role(str, Enum):
    ANALYST = "Analyst"
    SUPERVISOR = "Supervisor"



ALLOWED_TRANSITIONS = {
    (ComplaintStatus('Open'), ComplaintStatus('In Review')): (Role('Analyst'), Role('Supervisor')),
    (ComplaintStatus('In Review'), ComplaintStatus('Escalated')): (Role('Analyst'), Role('Supervisor')),
    (ComplaintStatus('Escalated'), ComplaintStatus('In Review')): (Role('Supervisor'),),                                                              
}

CLOSABLE = {
    (ComplaintStatus('In Review')): Role('Supervisor'),
    (ComplaintStatus('Escalated')): Role('Supervisor'),
}


APPROVAL_THRESHOLD_CAD = Decimal("1000.00")

def can_transition(current, target, role): 

    """True if `role` may move a complaint from `current` to `target` via PATCH.""" 
    if (current, target) in ALLOWED_TRANSITIONS:
        return True
    else:
        return False


"""
print(can_transition("Open", "In Review",'Supervisor' ))
print(can_transition("Open", "Closed",'Supervisor' ))
"""


def transition_problem(current, target, role): 

    """None if allowed, else the contract error code that explains why not: 

    INVALID_TRANSITION (no such transition) or FORBIDDEN_ROLE (wrong role).""" 
    if (current, target) not in ALLOWED_TRANSITIONS:
        return "INVALID_TRANSITION"
    elif (role) not in ALLOWED_TRANSITIONS[(current, target)]:
        return "FORBIDDEN_ROLE"
    else:
        return None




def needs_approval(compensation_cad): 

    """True when the amount is above CAD 1,000.00 (strictly above).""" 
    if compensation_cad > APPROVAL_THRESHOLD_CAD:
        return True
    else:
        return False

