from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from database import get_session
from Service.complaint_services.services import ComplaintService
from decimal import Decimal






router = APIRouter(prefix="/complaints", tags=["Read tools"])
"""T-03"""
session: Session = Depends(get_session)

@router.get("/{complaint_id}", operation_id="get_complaint")
def get_complaint(complaint_id: str, 
                  session: Session = Depends(get_session)):
    return ComplaintService(session).get_complaint(complaint_id)

"""T-08"""
@router.patch("/{complaint_id}/status", operation_id="change_status")
def change_status(complaint_id: str, 
                  target_status: str , 
                  reason: str, 
                  role: str, 
                  session: Session = Depends(get_session)):
    return ComplaintService(session).change_status(complaint_id, 
                                                   target_status, 
                                                   reason,
                                                   role)





""" create the complaint """

@router.post("/{complaint_id}/create", operation_id="create")
def create(customer_id: str,
           channel: str,
           category: str,
           complaint_text: str,
           priority: str,
           account_id: str,
           assigned_analyst_id: str,
           session: Session = Depends(get_session)):
     return ComplaintService(session).create(customer_id,
                                            channel,
                                            category,
                                            complaint_text,
                                            priority,
                                            account_id,
                                            assigned_analyst_id)   

"""T-09"""
@router.post("/{complaint_id}/close", operation_id="close")
def close(complaint_id: str, 
          compensation_cad: Decimal, 
          role: str,
          session: Session = Depends(get_session)):
    return ComplaintService(session).close(complaint_id, 
                                           compensation_cad, 
                                           role)