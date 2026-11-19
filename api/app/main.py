from database import import_data_sqlite, get_session
from sqlmodel import select, Session
from Models.customer import Customer
from Models.account import Account
from Models.employee import Employee
from Models.complaint import Complaint
from Models.complaint_status_history import ComplaintStatusHistory
from Repository.repositories import customer_repository, account_repository

from fastapi import FastAPI
from routes.complaints import router as complaints_router
from routes.customers import router as customers_router


app = FastAPI(title="Complaints API")
app.include_router(complaints_router)
app.include_router(customers_router)




"""
with get_session() as session:      
    accounts = session.exec(select(Account)).all()
    for a in accounts:
        print(a)"""