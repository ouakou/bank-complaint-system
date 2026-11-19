from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from database import get_session
from Service.complaint_services.services import ComplaintService





"""T-001 and T-002 (Exercise 3.2.2)."""



router = APIRouter(prefix="/customers", tags=["Read tools"])



@router.get("/{customer_id}", operation_id="get_customer")
def get_customer(customer_id : str, session: Session = Depends(get_session)):
    customer = ComplaintService(session).get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer

@router.get("/{customer_id}/accounts", operation_id="get_accounts")
def get_accounts(customer_id : str, session: Session = Depends(get_session)):
    return ComplaintService(session).get_accounts(customer_id)

