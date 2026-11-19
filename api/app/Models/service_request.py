from sqlmodel import SQLModel, Field, Relationship
from typing import List

class ServiceRequest(SQLModel, table=True):
    __tablename__ = "service_request"

    request_id: str = Field(primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id")
    account_id: str  = Field(foreign_key="account.account_id")
    request_type: str
    status: str
    created_at: str
    closed_at: str
