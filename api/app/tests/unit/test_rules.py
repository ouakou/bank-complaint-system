"""Exercise 3.4.1: every status pair for both roles, and the /close boundary.""" 

from decimal import Decimal 
from itertools import permutations 

import pytest

  

from domain.errors import ApprovalRequired, ForbiddenRole, InvalidTransition 
from Service.complaint_services.services import ComplaintService 
from tests.unit.fakes import FakeDB, FakeStore, fake_repositories 

  

STATUSES = ["Open", "In Review", "Pending Approval", "Escalated", "Closed"] 
# TODO ALLOWED: the 5 (current, target, role) cells PATCH allows (your "Fill in the grid on paper" grid) 

ALLOWED = {
    ("OPEN", "IN_PROGRESS", "Analyst"),
    ("OPEN", "IN_PROGRESS", "Supervisor"),
    ("IN_PROGRESS", "UNDER_REVIEW", "Analyst"),
    ("IN_PROGRESS", "UNDER_REVIEW", "Supervisor"),
    ("UNDER_REVIEW", "IN_PROGRESS", "Supervisor"),
}



# TODO WRONG_ROLE: the 1 cell whose transition exists but not for that role 

WRONG_ROLE = {("UNDER_REVIEW", "IN_PROGRESS", "Analyst")}

CELLS = [(a, b, role) for a, b in permutations(STATUSES, 2) for role in ("Analyst", "Supervisor")] 


def make_service(status): 

    store = FakeStore.sample() 
    store.complaints["CP00001"]["status"] = status 
    return ComplaintService(FakeDB(store), fake_repositories(store)), store 

def test_the_grid_has_40_cells(): 

    assert len(CELLS) == 40 and len(ALLOWED) == 5 and len(WRONG_ROLE) == 1 