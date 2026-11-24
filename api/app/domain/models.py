from enum import Enum
from decimal import Decimal
class ComplaintStatus(str, Enum): 

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    PENDING_APPROVAL = "PENDING_APPROVAL" 
    CLOSED = "CLOSED"

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Channel(str, Enum):
    PHONE = "Phone"
    WEB = "Web"
    EMAIL = "Email"
    BRANCH = "Branch"

class Category(str, Enum):
    FEE_DISPUTE = "Fee Dispute"
    SERVICE_DELAY = "Service Delay"
    TRANSACTION_ERROR = "Transaction Error"
    ONLINE_BANKING = "Online Banking"
    CARD_ISSUE = "Card Issue"
    CUSTOMER_SERVICE = "Customer Service"
    FRAUD_CLAIM = "Fraud Claim"


class Role(str, Enum):
    ANALYST = "Analyst"
    SUPERVISOR = "Supervisor"



ALLOWED_TRANSITIONS = {
    (ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS): (Role.ANALYST, Role.SUPERVISOR),
    (ComplaintStatus.IN_PROGRESS, ComplaintStatus.UNDER_REVIEW): (Role.ANALYST, Role.SUPERVISOR),
    (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.IN_PROGRESS): (Role.SUPERVISOR,),                                                              
}

CLOSABLE = {
    ComplaintStatus.IN_PROGRESS: Role.SUPERVISOR, 
    ComplaintStatus.UNDER_REVIEW: Role.SUPERVISOR
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

